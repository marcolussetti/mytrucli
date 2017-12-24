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
python3 grade_checker.py --username T00XXXXXX --password XXXXXX final_grades --term 201810
```

To check and get an email if any differences are detected
```bash
python grade_checker.py --username T00XXXXXX --password XXX final_grades --term 201810 --email XXX@XXXX.com --sendgrid-api-key SG.XXXXX
```
