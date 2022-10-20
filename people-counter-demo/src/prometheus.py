from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

from src.config import PeopleCounterConfig

PROM_DEPTHAI_JOB = 'depthai'


def send_count(count: int, cfg: PeopleCounterConfig):
    registry = CollectorRegistry()
    g = Gauge('people_count', 'People count', registry=registry, labelnames=['node_name'])
    g.labels(cfg.node_name).set(count)
    if cfg.push_gateway_addr:
        push_to_gateway(cfg.push_gateway_addr, job=PROM_DEPTHAI_JOB, registry=registry)


