import time
import os
import mh_z19

from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

PUSHGATEWAY_ADDRESS = os.getenv("PUSHGATEWAY_ADDRESS", "localhost:9091")
INTERVAL_SEC        = int(os.getenv("INTERVAL_SEC", "10"))


def main():
    print(f"PUSHGATEWAY_ADDRESS = {PUSHGATEWAY_ADDRESS}")
    print(f"INTERVAL_SEC        = {INTERVAL_SEC} second")
    while True:
        co2_conce = mh_z19.read_all()["co2"]
        send_co2_conce(co2_conce)
        time.sleep(INTERVAL_SEC)


def send_co2_conce(co2_conce: int):
    registry = CollectorRegistry()
    g = Gauge("co2_conce", "CO2 Conce", registry=registry)
    g.set(co2_conce)
    push_to_gateway(PUSHGATEWAY_ADDRESS, job="co2", registry=registry)


if __name__ == "__main__":
    main()
