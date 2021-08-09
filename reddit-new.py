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
			'username': '',
			'password': '',
			'redirect_url': 'http://localhost:8080',
			'start_from_today': False,
			'init-file' : str(Path(Path(__file__).parents[0] / 'inc' / 'init_time.txt'))	# Start where you left
			}

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

	# Start From Today or Recovery
	if CONFIG['start_from_today'] == False:
		# Read timestamp from file
		with open(CONFIG['init-file']) as f:
			unix_before = f.read()
		if unix_before == '':
			unix_before = str(int(time.time()))
	else:
		unix_before = str(int(time.time()))

	print(f"{logz.timestamp()}{Fore.GREEN} REDDIT → FETCH → {Style.RESET_ALL}Fetching Jokes. Going back from {dt.utcfromtimestamp(int(unix_before)).strftime('%Y-%m-%d %H:%M:%S')}")

	sort_type = 'score' # 'score'
	subreddit = 'jokes'
	size = 1000

	while True:
		time_start_get = time.time()
		url = f"https://api.pushshift.io/reddit/submission/search/?&subreddit={subreddit}&sort=desc&limit={size}&before={unix_before}"
		# url = f"https://api.pushshift.io/reddit/submission/search/?after={unix_after}&before={unix_before}&sort_type={sort_type}&sort=desc&subreddit={subreddit}&size={size}"
		# print(url)
		download_ok = False
		while not download_ok:
			try:
				r = requests.get(url)
				data = json.loads(r.text)
				r_json = data['data']
				time_end_get = time.time()
				download_ok = True
			except Exception as e:
				print(f"ERROR while fetch > {e}\nretry in 3sec")
				time.sleep(3.0)

		print(f"{logz.timestamp()}{Fore.GREEN} REDDIT → FETCH → {Style.RESET_ALL}{dt.utcfromtimestamp(int(r_json[0]['created_utc'])).strftime('%Y-%m-%d')} > {dt.utcfromtimestamp(int(r_json[-1]['created_utc'])).strftime('%Y-%m-%d')} = {size} Jokes fetched. Uploading to database... ({round(time_end_get - time_start_get, 2)}s)")

		# for post in r_json:#[-5:]:
		# 	if len(post['selftext']) > 240:
		# 		print(post)

		# print(len(r_json))

		# ----------------------------------------------

			#	#	#	#	#	#	#	#	#	#	#
			#										#
			#			UPLOAD TO DATABASE			#
			#										#
			#	#	#	#	#	#	#	#	#	#	#

		for post in r_json:
			# Check if new joke
			joke = postgres.get_joke_by_url(url=post['url'])

			# ------ FETCH DETAILS -------------------------

			# print(post)
			detailed_scan = False
			if detailed_scan == True:
				submission = reddit.submission(id=post['id'])
				# Check Upvote Ratio
				if hasattr(submission, 'upvote_ratio'):
					rating = submission.upvote_ratio
				else:
					rating = None
				post['num_comments'] = submission.num_comments
				post['score'] = submission.score
			else:
				rating = 0

			# Temp URL
			temp_url = post['url'].replace('https://www.reddit.com/r/Jokes/comments/', '')

			# Comments
			# submission.comment_sort = 'best'
			# top_level_comments = list(submission.comments)
			# # First Comment
			# for comment in top_level_comments:
			# 	# Only if has Upvotes
			# 	if hasattr(comment, 'ups'): # comment.ups
			# 		ups = 0
			# 	top_comment = {'author' : top_level_comments[0],
			# 					'ups': ups,
			# 					'content': comment.body,
			# 					'url': comment.permalink,
			# 					'time_add': dt.utcfromtimestamp(int(comment.created_utc)).strftime('%Y-%m-%d %H:%M:%S')
			# 					}
			# 	break

			# ------ NEW JOKE ------------------------------

			if joke == False:
				# Check if removed
				if 'selftext' not in post or post['selftext'] == '[removed]'  or post['selftext'] == '[deleted]':# or post['allow_live_comments'] == False:
					# print('Removed joke skipping')
					continue

				# print(f"ADD NEW > {temp_url}")

				# Check flair
				if 'link_flair_text' not in post:
					flair = None
				else:
					flair = post['link_flair_text']
				# Format Content
				temp_remove = ['&#x200B;']
				for char in temp_remove:
					post['selftext'] = post['selftext'].replace(char, '')
				# Clear HTML
				post['selftext'] = post['selftext'].replace('&amp;', '&').replace('&nbsp;', ' ')

				# 	# Add New Joke
				r = postgres.add_joke(time_add=None,
										time_add_original=dt.utcfromtimestamp(int(post['created_utc'])).strftime('%Y-%m-%d %H:%M:%S'),
										url=post['url'],
										author=post['author'],
										title=post['title'],
										content=post['selftext'],
										rating=rating, # None
										comment_count=post['num_comments'],
										vote_count=post['score'],
										language=None,
										shared_on_twitter=None,
										flair=flair)
				# if r == True:
				# 	# Add Comment
				# 	r = postgres.add_joke_comment(joke_id=r,
				# 									time_add=top_comment['time_add'],
				# 									url=top_comment['url'],
				# 									author=top_comment['author'],
				# 									content=top_comment['content'],
				# 									vote_count=top_comment['ups'],
				# 									lang=None)
			else:

				# ------ UPDATE RATING / COMMENTS / VOTE -------

				# print(f"UPDATE {temp_url}\trating={rating} comments={post['num_comments']} votes={post['score']}")
				# print('Updating rating, comments & vote count')
				# Update Rating
				r = postgres.set_joke_rating(joke_id=joke['id'], rating=rating)
				# Update Comment Count
				r = postgres.set_joke_comment_count(joke_id=joke['id'], comment_count=post['num_comments'])
				# Update Vote Count
				r = postgres.set_joke_vote_count(joke_id=joke['id'], vote_count=post['score'])

				# Update Time
				#
				#	INCOMPLETE - This Op. takes much time!
				#
				# r = postgres.set_joke_time_update(joke_id=joke['id'], time_update=None)




		# ----------------------------------------------
		#
		# CHECKPOINT
		#
		# Assign latest post time for go back point
		unix_before = r_json[-1]['created_utc']
		# Write timestamp to file
		with open(CONFIG['init-file'], 'w+') as out:
			out.write(str(unix_before))


if __name__ == '__main__':
	main()