import subprocess
import re
import time
import os

from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

PUSHGATEWAY_ADDRESS = os.getenv("PUSHGATEWAY_ADDRESS", "localhost:9091")


def main():
    for i in range(0, 100, 1):
    i = 0
    while True:
        co2_conce = get_co2_conce()
        send_co2_conce(co2_conce)
        print(f"{i}分経過: {co2_conce}")
        ++i
        time.sleep(60)


def get_co2_conce() -> int:
    out = subprocess.check_output(["sudo", "python3", "-m", "mh_z19"]).decode("utf-8")
    cmd_out = re.match(r"{\"co2\": (?P<conc>\d+)}", out)
    co2_conce = int(cmd_out.group("conc"))
    return co2_conce


def send_co2_conce(co2_conce: int):
    registry = CollectorRegistry()
    g = Gauge("co2_conce", "CO2 Conce", registry=registry)
    g.set(co2_conce)
    push_to_gateway(PUSHGATEWAY_ADDRESS, job="co2", registry=registry)


if __name__ == "__main__":
    main()
