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

Install systemd
```
# Edit installation location and other information
vi systemd/push-people-counter.service

sudo cp systemd/push-people-counter.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable push-people-counter
sudo systemctl start push-people-counter
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