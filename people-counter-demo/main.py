#!/usr/bin/env python3
from pathlib import Path

import blobconverter
import cv2
import depthai as dai
import numpy as np
import argparse
from time import monotonic
import itertools

from depthai_sdk import PipelineManager, NNetManager, PreviewManager
from depthai_sdk import cropToAspectRatio
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

parentDir = Path(__file__).parent

#=====================================================================================
# To use a different NN, change `size` and `nnPath` here:
size = (544, 320)
nnPath = blobconverter.from_zoo("person-detection-retail-0013", shaves=8)
#=====================================================================================

# Labels
labelMap = ["background", "person"]

# Get argument first
parser = argparse.ArgumentParser()
parser.add_argument('-d', '--debug', action="store_true",
                    help="Debug using camera view")
args = parser.parse_args()

# Whether we want to use images from host or rgb camera
nnSource = "color"

def main():

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
            frame = pv.get("color")

            nn_data = nm.decode(nm.outputQueue.get())
            nm.draw(frame, nn_data)
            print(len(nn_data))

            if args.debug:
                cv2.putText(frame, f"People count: {len(nn_data)}", (5, 30), cv2.FONT_HERSHEY_TRIPLEX, 1, (0,0,255))
                cv2.imshow("color", frame)

            if cv2.waitKey(1) == ord('q'):
                break

            if count > 10:
                count = 0
                send_count(len(nn_data))


def send_count(count: int):
    registry = CollectorRegistry()
    g = Gauge('people_count', 'People count', registry=registry)
    g.set(count)
    push_to_gateway('localhost:9091', job='depthai', registry=registry)


if __name__ == "__main__":
    main()
