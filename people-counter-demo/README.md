People Counter
-------------------

DelphAI demo based on [gen2-people-counter](https://github.com/luxonis/depthai-experiments/tree/master/gen2-people-counter)

## Requirements

Python3.9+

## Installation

```
python -m venv venv
. ./venv/bin/activate
pip install -r requirements.txt
```

Install systemd(node1)
```
sudo cp systemd/push-people-counter-node1.service /etc/systemd/system/push-people-counter.service
sudo cp systemd/collect-people-counter-node1.service /etc/systemd/system/collect-people-counter.service
sudo systemctl daemon-reload
sudo systemctl enable push-people-counter
sudo systemctl enable collect-people-counter
sudo systemctl start push-people-counter
sudo systemctl start collect-people-counter
```

Install systemd(node2)
```
sudo cp systemd/push-people-counter-node2.service /etc/systemd/system/push-people-counter.service
sudo cp systemd/collect-people-counter-node2.service /etc/systemd/system/collect-people-counter.service
sudo systemctl daemon-reload
sudo systemctl enable push-people-counter
sudo systemctl enable collect-people-counter
sudo systemctl start push-people-counter
sudo systemctl start collect-people-counter
```

## Usage

Run

```
./main.py collect_people_count
./main.py push_people_count [node_name]
```

Help

```
./main.py push_people_count -h
```

## License

MIT