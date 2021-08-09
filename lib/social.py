#! usr/bin/env python3
# -*- coding: utf-8 -*-
'''
#-------------------------------------------------------------------------------
Project		: Jaas
Module		: social
Purpose   	: Email API
Version		: 0.1.1 beta
Status 		: Development

Modified	: 2020 July 22
Created   	: 2020 July 22
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
from socket import gaierror
import os
import sys
import time
import json
import smtplib
sys.path.insert(0, str(Path(Path(__file__).parents[0] / 'lib')))
import logz
import facebook
from pyfacebook import Api, BaseModel

CONFIG = {	'facebook_page_id': '',
			'app-secret': '',
			'app-id': '',
			'page_access_token': '',
			}

def face(title, content):
	"""
	"""
	# Configure
	global CONFIG

	# Get Access Token
	api = Api(app_id=CONFIG['app-id'],
				app_secret=CONFIG['app-secret'],
				# short_token="short-lived token")
				long_term_token=CONFIG['page_access_token'])
	api.get_token_info()


	graph = facebook.GraphAPI(CONFIG['page_access_token'])
	graph.put_object(CONFIG['facebook_page_id'], "feed", message='test message')

	# ----------------------------------------------

	# Send
	try:
		graph.put_object(
		  parent_object=CONFIG['facebook_page_id'],
		  connection_name="feed",
		  message='I just posted automatically with python!',
		)
		return True
	except Exception as e:
		print(f"ERROR Couldn't be sent: {e}")
		return False

if __name__ == '__main__':
	face(title="Title of the post",
				content='Example FB post content')

