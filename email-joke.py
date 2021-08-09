#! usr/bin/env python3
# -*- coding: utf-8 -*-
'''
#-------------------------------------------------------------------------------
Project		: Project JaaS
Module		: email-joke
Purpose   	: Email Bot
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
from datetime import datetime as dt
from colorama import Fore, Back, Style
import os
import sys
import time
import json
import tweepy
import requests
import random
sys.path.insert(0, str(Path(Path(__file__).parents[0] / 'lib')))
import logz
import emailz
import postgres

CONFIG = {	# Filter
			'joke-length-min': 360,							# Joke must be @ least 280 chars
			'joke-length-max': 0,
			'joke-vote-count': 6000,						# Joke must has at least votes
			'joke-comment-count': 60,						# Joke must has at least comments
			'joke-rating': 0,								# 0.92 Joke must has at least rating/upvote ratio
			'joke-flair-forbidden': ['Politics'], #Religion		# Forbidden joke types
			'joke-words-forbidden': ['r/Jokes', 'subreddit'],
			}

def check_membership_status(user):
	"""
	"""
	time_now_unix = int(time.time())
	time_membership_end_unix = int(time.mktime(dt.strptime(user['membership_time_end'], "%Y-%m-%d %H:%M:%S").timetuple()))
	if time_membership_end_unix > time_now_unix:
		return True
	else:
		return False

def main():
	# Configure
	global CONFIG

	# Connect to DB
	postgres.connect_db()

	# Infinite Loop
	print(f"{logz.timestamp()}{Fore.MAGENTA} EMAIL → INIT → {Style.RESET_ALL}Waiting midnight to start", end='')
	last_run = dt.utcfromtimestamp(int(time.time() - 60 * 60 * 24)).strftime('%Y-%m-%d')
	while True:
		today = dt.utcfromtimestamp(int(time.time())).strftime('%Y-%m-%d')
		# Execute only @ 00:00 midnight
		if last_run == today:
			# Sleep
			time.sleep(60)
			# Check again
			continue

		# Record last run date
		last_run = today

		# ------ FETCH USERS ---------------------------

		# Start
		time_start = time.time()
		users = postgres.get_user_all()

		# ----------------------------------------------

			#	#	#	#	#	#	#	#	#	#	#
			#										#
			#			JOKE 			 			#
			#										#
			#	#	#	#	#	#	#	#	#	#	#

		# Fetch Jokes
		print(f"{logz.timestamp()}{Fore.MAGENTA} EMAIL → INIT → {Style.RESET_ALL}Fething all jokes...", end='')
		time_start_fetch = time.time()
		jokes = postgres.get_joke_all()
		# Shuffle
		random.shuffle(jokes)
		print(f" (~{str(len(jokes))[:3]}K) ({round(time.time() - time_start_fetch, 2)}s)")

		for user in users:

			# Check if user active membership
			if check_membership_status(user) == False:
				print(f"{logz.timestamp()}{Style.BRIGHT} EMAIL → CAUTION → {Style.RESET_ALL}User {user['id']} membership expired. Skipping")
				continue

			print(f"{logz.timestamp()}{Fore.MAGENTA} EMAIL → FILTER → {Style.RESET_ALL}Selecting joke for {user['full_name']} (id={user['id']})")
			for joke in jokes:

				# Check if joke sent before
				r = postgres.did_joke_send_before(joke_id=joke['id'],
													user_id=user['id'])
				if r != None: # isinstance(r, dict): # r != False
					time.sleep(1)
					continue

				# ------ FILTER  -------------------------------

				if (len(joke['title']) + len(joke['content']) > CONFIG['joke-length-min']
					and (joke['vote_count'] >= CONFIG['joke-vote-count'])
					and (joke['comment_count'] >= CONFIG['joke-comment-count'])
					and (joke['rating'] >= CONFIG['joke-rating'])
					and (joke['flair'] not in CONFIG['joke-flair-forbidden'])):

					# Check
					for forbidden_word in CONFIG['joke-words-forbidden']:
						if forbidden_word.lower() in joke['title'] or forbidden_word.lower() in joke['content']:
							print(f'word {forbidden_word.lower()} is forbidden. skipping joke')
							continue

					print(f"{logz.timestamp()}{Fore.MAGENTA} EMAIL → FILTER → {Style.RESET_ALL}Selected Joke {joke['id']}")#  title:{joke['title']}

					# Select
					joke_selected = joke
					# Select Emoji
					emoji = random.choice(['🤣','😆','😂','😅','😁','😄','😝'])

					# ------ CONSTRUCT JOKE  -----------------------

					# print(f"{joke_selected['title']}\n{joke_selected['content']}\n\n\n\n------\n\n")
					email_joke = f"""{joke_selected['title']}\n
									{joke_selected['content']} {emoji}\n\n\n
									———————
									Hi {user['full_name'].split(' ')[0]}. This joke is for your daily digest. I hope you liked it.<p>
									I sent you this email because you are member of our exclusive joke club 🤫"""

					# Trim Title
					joke['title'] = f"🤩 {joke['title']}"
					if len(joke['title']) >= 77:
						joke['title'] = f"{joke['title'][:77]}..."

					# ------ SEND EMAIL ----------------------------

					print(f"{logz.timestamp()}{Fore.MAGENTA} EMAIL → SENDING → {Style.RESET_ALL}Joke {joke['id']} to {user['full_name']})")
					emailz.send_email(receiver=user['email'],
										subject=joke['title'],
										content=email_joke)

					# ------ MARK AS SENT --------------------------

					# Mark as emailed
					r =  postgres.add_joke_send(joke_id=joke['id'],
												user_id=user['id'],
												time_send=None)

					print(f"{logz.timestamp()}{Fore.MAGENTA} EMAIL → SENT → {Style.RESET_ALL}Marked as sent")

					# Exit
					break

				else:
					pass
					# print(f"{logz.timestamp()}{Fore.MAGENTA} EMAIL → FILTER → {Style.RESET_ALL}Joke {joke['id']} below params. Skipping")

		# ----------------------------------------------

		print(f"{logz.timestamp()}{Fore.MAGENTA} EMAIL → INIT → {Style.RESET_ALL}Waiting midnight to start", end='')

		# ----------------------------------------------

if __name__ == '__main__':
	main()
