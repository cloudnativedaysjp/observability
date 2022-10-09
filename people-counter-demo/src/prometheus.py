from prometheus_client import CollectorRegistry, Gauge, push_to_gateway


def send_count(count: int, addr: str):
    registry = CollectorRegistry()
    g = Gauge('people_count', 'People count', registry=registry)
    g.set(count)
    push_to_gateway(addr, job='depthai', registry=registry)


