#!/usr/bin/env python3
import fire

from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

from src.depthai import DepthAi, DepthAiConfig


class Command:

    def people_count(
            self,
            push_gateway_addr: str = '',
            debug: bool = False
    ):
        cfg = DepthAiConfig(
            push_gateway_addr=push_gateway_addr,
            debug=debug
        )
        d = DepthAi(cfg)
        d.run()


if __name__ == "__main__":
    fire.Fire(Command)
