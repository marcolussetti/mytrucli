# mytrucli
**Important note:** this is an early work in progress, and is not really setup to work cross-platform yet. I'll write up better instructions soon(TM).

## Quickstart
### Setup
#### Ubuntu 16.04
```bash
# Clone Repo
git clone https://github.com/marcolussetti/mytrucli.git
cd mytrucli

# Install requirements
sudo apt-get install firefox
wget https://github.com/mozilla/geckodriver/releases/download/v0.19.1/geckodriver-v0.19.1-linux64.tar.gz
tar -xvzf geckodriver-v0.19.1-linux64.tar.gz
sudo mv geckodriver /usr/local/bin
rm geckodriver-v0.19.1-linux64.tar.gz

pip install --user pipenv
~/.local/bin/pipenv --three install -r requirements.txt
```

#### Arch Linux

```bash
git clone https://github.com/marcolussetti/mytrucli.git
cd mytrucli

sudo pacman -S firefox
pacaur -S geckodriver  # Or whatever AUR helper you use

pip install --user pipenv
~/.local/bin/pipenv --three install -r requirements.txt
```


### Execution

#### Final Grades Checker

To console:

```bash
~/.local/bin/pipenv run python mytrucli.py --username T00XXXXXX --password 
XXXXXX 
final_grades --term 201810
```

To email:

```bash
~/.local/bin/pipenv run python mytrucli.py --username T00XXXXXX --password 
XXXXXX --email XXX@XXXX.com --sendgrid-api-key SG.XXXXX final_grades --term 
201810
```

As a cronjob (every 15 minutes):

```bash
ls ~/.virtualenvs

sudo vim /etc/crontab
# This is to be appended then
*/15 * * * * USERNAME cd /home/USERNAME/mytrucli && /home/USERNAME/
.virtualenvs/mytru-SEEOUTPUTOFABOVE/python mytrucli.py --username T00XXXXXX --password 
XXXXXX --email XXX@XXXX.com --sendgrid-api-key SG.XXXXX final_grades --term 
201810 &>> /tmp/mytrucli.log
```

#### Moodle Grades Checker

The `course` parameter refers to the Moodle ID for that course.

To console:

```bash
~/.local/bin/pipenv run python mytrucli.py --username T00XXXXXX --password 
XXXXXX 
moodle_grades --course 7400
```

To email:

```bash
~/.local/bin/pipenv run python mytrucli.py --username T00XXXXXX --password 
XXXXXX --email XXX@XXXX.com --sendgrid-api-key SG.XXXXX moodle_grades --course 
7400
```


As a cronjob (every 15 minutes):

```bash
ls ~/.virtualenvs

sudo vim /etc/crontab
# This is to be appended then
*/15 * * * * USERNAME cd /home/USERNAME/mytrucli && /home/USERNAME/
.virtualenvs/mytru-SEEOUTPUTOFABOVE/python mytrucli.py --username T00XXXXXX --password 
XXXXXX --email XXX@XXXX.com --sendgrid-api-key SG.XXXXX moodle_grades --course 
7400 &>> /tmp/mytrucli.log
```

#### Moodle Assignments Checker

The `course` parameter refers to the Moodle ID for that course.

To console:

```bash
~/.local/bin/pipenv run python mytrucli.py --username T00XXXXXX --password 
XXXXXX 
moodle_assignments --course 7400
```

### Cronjob issues
Exceptions and Errors in Selenium are not yet handle (beyond the 30s wait time), so if Selenium crashes on a cronjob you have Firefox instances piling up.

As a very dirty cleanup job on a server where firefox is not used for anything else, you can use:
```bash
sudo vim /etc/crontab
# This is to be appended then
3,18,33,48 * * * * USERNAME pkill firefox
```