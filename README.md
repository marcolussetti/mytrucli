# mytrucli
**Important note:** this is an early work in progress, and is not really setup to work cross-platform yet. I'll write up better instructions soon(TM).

## Setup
It needs firefox and geckodriver for now. Geckodriver needs to be in the path.

```bash
pacaur -S geckodriver
```

```bash
pip install -r requirements.txt
```

## Execution
To check final grades for Fall 2018
```bash
python3 grade_checker.py --username T00XXXXXX --password XXXXXX --term 201810
```
