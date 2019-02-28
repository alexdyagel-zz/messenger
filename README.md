# Nostromo
Nostromo is used for testing Tiobe index page (https://www.tiobe.com/tiobe-index/) and a little bit of blank.org website.
### Installation
Nostromo requires [requests](http://docs.python-requests.org/en/master/), [beautifulsoup4](https://pypi.org/project/beautifulsoup4/) and [pytest](https://docs.pytest.org/en/latest/) for valid run.
Installing example: 
```sh
$ pipenv install requests
$ pip install -U pytest
$ pip install beautifulsoup4
```

### Run Nostromo

There are several ways to run Nostromo.

First way (for consistent execution of tests):
```sh
$ py.test test_tiobe.py
```

Second way (for parallel execution of tests):
```sh
$ pytest -n auto
```