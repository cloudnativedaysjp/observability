#!/usr/bin/env python3
import fire

from src.config import PeopleCounterConfig
from src.depthai import DepthAiPeopleCounter


class Command:

    def people_count(
            self,
            node_name: str,
            push_gateway_addr: str = '',
            push_period_seconds: int = 1,
            debug: bool = False
    ):
        """
        Collect people count using DepthAI

        :param node_name: A node identifier to be used as Prometheus label.
        :param push_gateway_addr: An address of Prometheus Push-gateway
        :param push_period_seconds: Time period in seconds to push people-count metric to Push-gateway
        :param debug: Show debug camera view.
        """

        cfg = PeopleCounterConfig(
            node_name=node_name,
            push_gateway_addr=push_gateway_addr,
            push_period_seconds=push_period_seconds,
            debug=debug
        )
        people_counter = DepthAiPeopleCounter(cfg)
        people_counter.run()


if __name__ == "__main__":
    fire.Fire(Command)
