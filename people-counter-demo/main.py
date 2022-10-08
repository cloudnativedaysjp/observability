#!/usr/bin/env python3
import fire

from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

from src.depthai import DepthAi

class Command:

    def people_count(
            self,
            push_gateway_addr: str = '',
            debug: bool = False
    ):
        d = DepthAi()
        d.run(debug)


def send_count(count: int, addr: str):
    registry = CollectorRegistry()
    g = Gauge('people_count', 'People count', registry=registry)
    g.set(count)
    push_to_gateway(addr, job='depthai', registry=registry)


if __name__ == "__main__":
    fire.Fire(Command)
