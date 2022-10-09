import math
from dataclasses import dataclass
from datetime import datetime
from typing import Callable

import blobconverter
import cv2
import depthai as dai
from depthai_sdk import PipelineManager, NNetManager, PreviewManager
import numpy as np

from src.config import PeopleCounterConfig
from src.prometheus import send_count
from src.queue import SimpleQueue

# To use a different NN, change `size` and `nnPath` here:
size = (544, 320)
nnPath = blobconverter.from_zoo("person-detection-retail-0013", shaves=8)
nnSource = "color"

# Labels
labelMap = ["background", "person"]


class DepthAiPeopleCounter:
    cfg: PeopleCounterConfig
    pm: PipelineManager
    pv: PreviewManager
    nm: NNetManager

    _q: SimpleQueue
    _should_quit: bool = False

    def __init__(self, cfg: PeopleCounterConfig):
        self.cfg = cfg
        self.pm = PipelineManager()
        self.pm.createColorCam(previewSize=size, xout=True)
        self.pv = PreviewManager(display=["color"], nnSource=nnSource)

        self.nm = NNetManager(inputSize=size, nnFamily="mobilenet", labels=labelMap, confidence=0.5)
        nn = self.nm.createNN(self.pm.pipeline, self.pm.nodes, blobPath=nnPath, source=nnSource)
        self.pm.setNnManager(self.nm)
        self.pm.addNn(nn)

        self._q = SimpleQueue(self.cfg.push_period_seconds)

    def run(self):
        with dai.Device(self.pm.pipeline) as device:
            self.nm.createQueues(device)
            self.pv.createQueues(device)

            while True:
                if self._should_quit:
                    break

                self.pv.prepareFrames(blocking=True)
                nn_data = self.nm.decode(self.nm.outputQueue.get())
                self._q.add(len(nn_data))

                if self.cfg.debug:
                    self._show_frame(nn_data)

                self._q.run_after_period(self._send_count)

    def _send_count(self, counts: list[int]) -> bool:
        avg_count = math.ceil(np.average(counts))
        print(f"{datetime.now()}: {avg_count} count - {counts}")
        if not self.cfg.push_gateway_addr:
            return True
        try:
            send_count(avg_count, self.cfg)
            return True
        except RuntimeError as e:
            print(e)
            return False

    def _show_frame(self, nn_data):
        frame: np.ndarray = self.pv.get("color")
        self.nm.draw(frame, nn_data)
        cv2.putText(frame, f"People count: {len(nn_data)}", (5, 30), cv2.FONT_HERSHEY_TRIPLEX, 1,
                    (0, 0, 255))
        cv2.imshow("color", frame)
        self._check_quit()

    def _check_quit(self):
        if cv2.waitKey(1) == ord('q'):
            self._should_quit = True
