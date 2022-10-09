from dataclasses import dataclass

import blobconverter
import cv2
import depthai as dai
from depthai_sdk import PipelineManager, NNetManager, PreviewManager

# To use a different NN, change `size` and `nnPath` here:
size = (544, 320)
nnPath = blobconverter.from_zoo("person-detection-retail-0013", shaves=8)

# Labels
labelMap = ["background", "person"]

nnSource = "color"


@dataclass
class DepthAiConfig:
    push_gateway_addr: str = '',
    debug: bool = False


class DepthAi:
    cfg: DepthAiConfig

    pm: PipelineManager
    pv: PreviewManager
    nm: NNetManager



    def __init__(self, cfg: DepthAiConfig):
        self.cfg = cfg
        self.pm = PipelineManager()
        self.pm.createColorCam(previewSize=size, xout=True)
        self.pv = PreviewManager(display=["color"], nnSource=nnSource)

        self.nm = NNetManager(inputSize=size, nnFamily="mobilenet", labels=labelMap, confidence=0.5)
        nn = self.nm.createNN(self.pm.pipeline, self.pm.nodes, blobPath=nnPath, source=nnSource)
        self.pm.setNnManager(self.nm)
        self.pm.addNn(nn)

    def run(self, debug: bool):
        with dai.Device(self.pm.pipeline) as device:
            self.nm.createQueues(device)
            self.pv.createQueues(device)

            while True:
                self.pv.prepareFrames(blocking=True)
                nn_data = self.nm.decode(self.nm.outputQueue.get())
                print(len(nn_data))
                if debug:
                    self._show_frame(nn_data)
                    if self._check_quit():
                        break

    def _show_frame(self, nn_data):
        frame = self.pv.get("color")
        self.nm.draw(frame, nn_data)
        cv2.putText(frame, f"People count: {len(nn_data)}", (5, 30), cv2.FONT_HERSHEY_TRIPLEX, 1,
                    (0, 0, 255))
        cv2.imshow("color", frame)

    def _check_quit(self) -> bool:
        if cv2.waitKey(1) == ord('q'):
            return True
        return False