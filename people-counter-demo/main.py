#!/usr/bin/env python3
import blobconverter
import cv2
import depthai as dai
import fire

from depthai_sdk import PipelineManager, NNetManager, PreviewManager
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

#=====================================================================================
# To use a different NN, change `size` and `nnPath` here:
size = (544, 320)
nnPath = blobconverter.from_zoo("person-detection-retail-0013", shaves=8)
#=====================================================================================

# Labels
labelMap = ["background", "person"]

# Whether we want to use images from host or rgb camera
nnSource = "color"


class Command:

    def people_count(
            self,
            push_gateway_addr: str = '',
            debug: bool = False
    ):
        # Start defining a pipeline
        pm = PipelineManager()
        pm.createColorCam(previewSize=size, xout=True)
        pv = PreviewManager(display=["color"], nnSource=nnSource)

        nm = NNetManager(inputSize=size, nnFamily="mobilenet", labels=labelMap, confidence=0.5)
        nn = nm.createNN(pm.pipeline, pm.nodes, blobPath=nnPath, source=nnSource)
        pm.setNnManager(nm)
        pm.addNn(nn)

        # Pipeline defined, now the device is connected to
        with dai.Device(pm.pipeline) as device:
            nm.createQueues(device)
            pv.createQueues(device)

            count = 0
            while True:
                count += 1
                pv.prepareFrames(blocking=True)

                nn_data = nm.decode(nm.outputQueue.get())
                print(len(nn_data))

                if debug:
                    frame = pv.get("color")
                    nm.draw(frame, nn_data)
                    cv2.putText(frame, f"People count: {len(nn_data)}", (5, 30), cv2.FONT_HERSHEY_TRIPLEX, 1,
                                (0, 0, 255))
                    cv2.imshow("color", frame)

                    if cv2.waitKey(1) == ord('q'):
                        break

                if count > 10:
                    count = 0
                    if push_gateway_addr:
                        send_count(len(nn_data), push_gateway_addr)


def send_count(count: int, addr: str):
    registry = CollectorRegistry()
    g = Gauge('people_count', 'People count', registry=registry)
    g.set(count)
    push_to_gateway(addr, job='depthai', registry=registry)


if __name__ == "__main__":
    fire.Fire(Command)
