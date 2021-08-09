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
import os
import sys
import time
import json
import requests
import random
import praw
import requests
import traceback
from datetime import datetime
from psaw import PushshiftAPI

CONFIG = {'secret_key': '',
			'personal_key': '',
			'name': 'jaas_dev',
			'username': '',
			'password': '',
			'redirect_url': 'http://localhost:8080'}


username = ""

url = "https://api.pushshift.io/reddit/{}/search?limit=1000&sort=desc&author={}&before="

start_time = datetime.utcnow()


def downloadFromUrl(filename, object_type):
	print(f"Saving {object_type}s to {filename}")

	count = 0
	handle = open(filename, 'w')
	previous_epoch = int(start_time.timestamp())
	while True:
		new_url = url.format(object_type, username)+str(previous_epoch)
		json = requests.get(new_url) # headers={'User-Agent': "Post downloader by /u/Watchful1"}
		json_data = json.json()
		if 'data' not in json_data:
			break
		objects = json_data['data']
		if len(objects) == 0:
			break

		for object in objects:
			previous_epoch = object['created_utc'] - 1
			count += 1
			if object_type == 'comment':
				try:
					handle.write(str(object['score']))
					handle.write(" : ")
					handle.write(datetime.fromtimestamp(object['created_utc']).strftime("%Y-%m-%d"))
					handle.write("\n")
					text = object['body']
					textASCII = text.encode(encoding='ascii', errors='ignore').decode()
					handle.write(textASCII)
					handle.write("\n-------------------------------\n")
				except Exception as err:
					print(f"Couldn't print comment: https://www.reddit.com{object['permalink']}")
					print(traceback.format_exc())
			elif object_type == 'submission':
				if object['is_self']:
					if 'selftext' not in object:
						continue
					try:
						handle.write(str(object['score']))
						handle.write(" : ")
						handle.write(datetime.fromtimestamp(object['created_utc']).strftime("%Y-%m-%d"))
						handle.write("\n")
						text = object['selftext']
						textASCII = text.encode(encoding='ascii', errors='ignore').decode()
						handle.write(textASCII)
						handle.write("\n-------------------------------\n")
					except Exception as err:
						print(f"Couldn't print post: {object['url']}")
						print(traceback.format_exc())

		print("Saved {} {}s through {}".format(count, object_type, datetime.fromtimestamp(previous_epoch).strftime("%Y-%m-%d")))

	print(f"Saved {count} {object_type}s")
	handle.close()


downloadFromUrl("posts.txt", "submission")
downloadFromUrl("comments.txt", "comment")



if __name__ == '__main__':
	main()