from dataclasses import dataclass

METRIC_FILE = "./metric"


@dataclass
class PeopleCounterConfig:
    node_name: str
    push_gateway_addr: str = '',
    push_period_seconds: int = 1
    debug: bool = False
