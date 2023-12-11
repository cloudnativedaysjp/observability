from dataclasses import dataclass

METRIC_FILE = "./metric"


@dataclass
class PeopleCounterConfig:
    period_seconds: int = 1
    debug: bool = False

@dataclass
class ExporterConfig:
    node_name: str
    job_name: str
    push_gateway_addr: str = ''
    push_period_seconds: int = 1
    debug: bool = False
