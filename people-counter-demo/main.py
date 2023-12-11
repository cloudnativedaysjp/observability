#!/usr/bin/env python3
import fire

from src.config import PeopleCounterConfig, ExporterConfig
from src.prometheus import MetricExporter, PROM_DEPTHAI_JOB


class Command:

    def collect_people_count(
            self,
            period_seconds: int = 1,
            debug: bool = False
    ):
        """
        Collect people count using DepthAI
        :param period_seconds: Time period in seconds to push people-count metric to Push-gateway
        :param debug: Show debug camera view.
        """

        cfg = PeopleCounterConfig(
            period_seconds=period_seconds,
            debug=debug
        )

        from src.depthai import DepthAiPeopleCounter
        people_counter = DepthAiPeopleCounter(cfg)

        try:
            people_counter.run()
        except Exception as e:
            print(e)

    def push_people_count(
            self,
            node_name: str,
            job_name: str = PROM_DEPTHAI_JOB,
            push_gateway_addr: str = '',
            push_period_seconds: int = 1,
            debug: bool = False
    ):
        """
        Push people count using DepthAI

        :param node_name: A node identifier to be used as Prometheus label.
        :param job_name: A job identifier to be used as Prometheus label.
        :param push_gateway_addr: An address of Prometheus Push-gateway
        :param push_period_seconds: Time period in seconds to push people-count metric to Push-gateway
        :param debug: Show debug camera view.
        """

        cfg = ExporterConfig(
            node_name=node_name,
            job_name=job_name,
            push_gateway_addr=push_gateway_addr,
            push_period_seconds=push_period_seconds,
            debug=debug
        )
        exporter = MetricExporter(cfg)

        try:
            exporter.run()
        except Exception as e:
            print(e)


if __name__ == "__main__":
    fire.Fire(Command)
