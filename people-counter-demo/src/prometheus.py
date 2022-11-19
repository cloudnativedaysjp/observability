from multiprocessing import Process
from time import sleep

from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

from src.config import PeopleCounterConfig, METRIC_FILE

PROM_DEPTHAI_JOB = 'depthai'


def send_count(count: int, cfg: PeopleCounterConfig):
    registry = CollectorRegistry()
    g = Gauge('people_count', 'People count', registry=registry, labelnames=['node_name'])
    g.labels(cfg.node_name).set(count)
    if cfg.push_gateway_addr:
        try:
            push_to_gateway(cfg.push_gateway_addr, job=PROM_DEPTHAI_JOB, registry=registry)
            print(f"sent to prometheus: {count}")
        except Exception as e:
            print(e)
    else:
        print(f"dry-run mode: {count}")


class MetricExporter(Process):
    cfg: PeopleCounterConfig

    def __init__(self, cfg: PeopleCounterConfig):
        super().__init__()
        self.cfg = cfg

    def run(self):
        while True:
            with open(METRIC_FILE) as f:
                try:
                    count = f.read()
                except Exception as e:
                    print(e)
            send_count(int(count), self.cfg)
            sleep(1)
