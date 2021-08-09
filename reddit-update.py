#! usr/bin/env python3
# -*- coding: utf-8 -*-
'''
#-------------------------------------------------------------------------------
Project		: Project JaaS
Module		: reddit
Purpose   	: Reddit API Wrapper
Version		: 0.1.1 beta
Status 		: Development

Modified	: 2020 Mar 04
Created   	: 2020 Mar 04
Author		: Burak Tokman
Email 		: buraktokman@hotmail.com
Copyright 	: 2020, Bulrosa OU
Licence   	: EULA
			  Unauthorized copying of this file, via any medium is strictly prohibited
			  Proprietary and confidential
#-------------------------------------------------------------------------------
'''

from pathlib import Path
from psaw import PushshiftAPI
from datetime import datetime as dt
from colorama import Fore, Back, Style
import os
import sys
import time
import threading
import json
import requests
import random
import praw
sys.path.insert(0, str(Path(Path(__file__).parents[0] / 'lib')))
import logz
import postgres

# Reddit Dev > https://www.reddit.com/prefs/apps

CONFIG = {'secret_key': '',
			'personal_key': '',
			'name': 'jaas_dev',
			'username': '', # Reddit User
			'password': '',
			'redirect_url': 'http://localhost:8080',
			'thread-count': 8,
			# 'refresh-interval': 24 * 60 # hours
			}

def thread_update(reddit, jokes):

	print(f"{logz.timestamp()}{Fore.YELLOW} REDDIT → INIT → {Style.RESET_ALL}Skip posts older than 30 days", end='')
	print(f"{logz.timestamp()}{Fore.YELLOW} REDDIT → INIT → {Style.RESET_ALL}Skip posts updated within 1 day", end='')
	for joke in jokes:

		#
		#	INCOMPLETE
		#
		# Skip if older then 30 days
		time_diff_unix = int(time.time()) - int(time.mktime(dt.strptime(joke['time_add_original'], "%Y-%m-%d %H:%M:%S").timetuple()))
		if 60 * 60 * 24 * 30 > time_diff_unix:
			# print(f"f_id={joke['id']} > skip. cuz not posted within 30 days")
			continue

		# Skip if updated in last 30 days
		if joke['time_update'] != None:
			time_diff_unix = int(time.time()) - int(time.mktime(dt.strptime(joke['time_update'], "%Y-%m-%d %H:%M:%S").timetuple()))
			if 60 * 60 * 24 * 1 > time_diff_unix:
				# print(f"f_id={joke['id']} > skip. cuz updated within 30 days")
				continue

		# https://www.reddit.com/r/Jokes/comments/coj45m/if_your_surprised_that_jeffrey_epstein_commited/
		j_id = joke['url'].split('comments/')[1].split('/')[0]

		submission = reddit.submission(id=j_id)
		# Check Upvote Ratio
		if hasattr(submission, 'upvote_ratio'):
			rating = submission.upvote_ratio
		else:
			rating = None

		# ------ UPDATE RATING / COMMENTS / VOTE -------

		print(f"UPDATE {j_id}\trating={rating}\tcomments={submission.num_comments}\tvotes={submission.score}")
		# print('Updating rating, comments & vote count')
		# Update Rating
		r = postgres.set_joke_rating(joke_id=joke['id'], rating=rating)
		# Update Comment Count
		r = postgres.set_joke_comment_count(joke_id=joke['id'], comment_count=submission.num_comments)
		# Update Vote Count
		r = postgres.set_joke_vote_count(joke_id=joke['id'], vote_count=submission.score)

		# Update Time
		#
		#	INCOMPLETE - This Op. takes much time!
		#
		r = postgres.set_joke_time_update(joke_id=joke['id'], time_update=None)

	print('thread finished')


def main():
	# Configure
	global CONFIG
	reddit = praw.Reddit(client_id=CONFIG['personal_key'],
						 client_secret=CONFIG['secret_key'],
						 user_agent=CONFIG['name'],
						 username=CONFIG['username'],
						 password=CONFIG['password'])

	# Connect to DB
	postgres.connect_db()

	# Start Fetch
	time_start = time.time()

	# Fetch Jokes
	print(f"{logz.timestamp()}{Fore.YELLOW} REDDIT → INIT → {Style.RESET_ALL}Fething all jokes...")
	jokes = postgres.get_joke_all()

	# ------------- MULTIPLE THREADS ---------------

	if CONFIG['thread-count'] != 1:
		jokes_thread = [jokes[i::CONFIG['thread-count']] for i in range(CONFIG['thread-count'])]
	else:
		jokes_thread = [jokes]

	print(f"{logz.timestamp()}{Fore.YELLOW} REDDIT → {Style.RESET_ALL}Starting threads")
	# Define threads
	threads = []

	for x in range(0, CONFIG['thread-count']):
		thread_name = 'T' + str(x) + '-update-jokes'
		t = threading.Thread(name=thread_name, target=thread_update, args=(reddit, jokes_thread[x], ))
		threads.append(t)
	# Start threads
	for x in range(0, CONFIG['thread-count']):
		# print(f"{logz.timestamp()}{Fore.YELLOW} REDDIT → {Style.RESET_ALL}THREAD {x} → Started")
		threads[x].start()
	# Wait threads
	for x in range(0, CONFIG['thread-count']):
		threads[x].join()
		# print(f"{logz.timestamp()}{Fore.YELLOW} REDDIT → {Style.RESET_ALL}Thread {x} finished in {round((time.time() - time_start) / 60, 2)} mins")
	print(f"{logz.timestamp()}{Fore.YELLOW} REDDIT → {Style.RESET_ALL}All threads finished in {round((time.time() - time_start) / 60, 2)} mins")
	# ------ SLEEP ---------------------------------

    # print(f"{logz.timestamp()}{Fore.YELLOW} REDDIT → COMPLETED → {Style.RESET_ALL}Sleeping {CONFIG['refresh-interval'] * 60}mins")
    # time.sleep(CONFIG['refresh-interval'] * 60)

	# ----------------------------------------------

if __name__ == '__main__':
	main()