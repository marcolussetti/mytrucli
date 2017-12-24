# mytrucli
**Important note:** this is an early work in progress, and is not really setup to work cross-platform yet. I'll write up better instructions soon(TM).

## Ubuntu 16.04 Quickstart
### Setup
```bash
# Clone Repo
git clone https://github.com/marcolussetti/mytrucli.git
cd mytrucli

# Install requirements
apt-get install firefox
wget https://github.com/mozilla/geckodriver/releases/download/v0.19.1/geckodriver-v0.19.1-linux64.tar.gz
tar -xvzf geckodriver-v0.19.1-linux64.tar.gz
sudo mv geckodriver /usr/local/bin
rm geckodriver-v0.19.1-linux64.tar.gz

pip install --user pipenv
~/.local/bin/pipenv --three install -r requirements.txt
```
### Execution

```bash
~/.local/bin/pipenv run python grade_checker.py --username T00XXXXXX --password XXXXXX final_grades --term 201810
```

### Cronjob (as user)
```bash
crontab -u USERNAME -e
# This is to be appended then
1,31 * * * * cd /home/USERNAME/mytrucli && /home/USERNAME/.local/bin/pipenv run python grade_checker.py --username T00XXXXXX --password XXXXX final_grades --term 201810 --email XXX@XXXX.com --sendgrid-api-key SG.XXXX > /tmp/mytrucli.log
```

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
