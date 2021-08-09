# Reddit-Jokes [![GitHub stars](https://img.shields.io/github/stars/badges/shields.svg?style=social&label=Stars)](https://github.com/buraktokman/Reddit-Jokes/)

[![Travis](https://img.shields.io/travis/rust-lang/rust.svg)](https://github.com/buraktokman/Reddit-Jokes)
[![Repo](https://img.shields.io/badge/source-GitHub-303030.svg?maxAge=3600&style=flat-square)](https://github.com/buraktokman/Reddit-Jokes)
[![Requires.io](https://img.shields.io/requires/github/celery/celery.svg)](https://requires.io/github/buraktokman/Reddit-Jokes/requirements/?branch=master)
[![Scrutinizer](https://img.shields.io/scrutinizer/g/filp/whoops.svg)](https://github.com/buraktokman/Reddit-Jokes)
[![DUB](https://img.shields.io/dub/l/vibe-d.svg)](https://choosealicense.com/licenses/mit/)
[![Donate with Bitcoin](https://img.shields.io/badge/Donate-BTC-orange.svg)](https://blockchain.info/address/17dXgYr48j31myKiAhnM5cQx78XBNyeBWM)
[![Donate with Ethereum](https://img.shields.io/badge/Donate-ETH-blue.svg)](https://etherscan.io/address/91dd20538de3b48493dfda212217036257ae5150)

Download jokes and hilarious stories from reddit.com/r/Jokes and send the most upvoted jokes to users that have an active email subscription.

### USAGE:
------
Before using import Postgres database backup included in **database** folder.

Modify the scripts to include Reddit and email credentials you want to used by scripts.


### Instructions
------

0. Fork, clone or download this repository

    `git clone https://github.com/buraktokman/Reddit-Jokes.git`

1. Navigate to the directory

    `cd Reddit-Jokes`

2. Install requirements

    `pip install -r requirements.txt`

3. Run the scripts in order on seperate terminals

    `python3 reddit-new.py`
    `python3 reddit-update.py`
    `python3 email-joke.py`
    `python3 membership-manager.py`

### LICENSE
------

MIT License
