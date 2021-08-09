#! usr/bin/env python3
# -*- coding: utf-8 -*-
'''
#-------------------------------------------------------------------------------
Project		: Project JaaS
Module		: emailz
Purpose   	: Email API
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
from socket import gaierror
from email.mime.text import MIMEText
import os
import sys
import time
import json
import smtplib
sys.path.insert(0, str(Path(Path(__file__).parents[0] / 'lib')))
import logz
import postgres
import twitter

CONFIG = {	'senders-name': 'Jaas ',
			'email-address': '',
			'email-password': '',
			'smtp-server': 'smtpout.secureserver.net',
			'smtp-port': 80, # SSL 465
			'html-template' : str(Path(Path(__file__).parents[1] / 'inc' / 'email-template' / 'email.html'))
			}

def send_email(receiver, subject, content):
	"""
	"""
	# Configure
	global CONFIG

	# Login
	# print('login')
	smtpserver = smtplib.SMTP(CONFIG['smtp-server'], CONFIG['smtp-port'])
	smtpserver.ehlo
	smtpserver.login(CONFIG['email-address'], CONFIG['email-password'])

	# ----------------------------------------------

	# Header
	# header = 'To:' + receiver + '\n' + 'From: ' + CONFIG['email-address'] + '\n' + 'Subject:testing \n'
	# print(header)

	# Load HTML Template
	with open(CONFIG['html-template']) as f:
		html_template = f.read()

	# Content
	content = content.replace('\n', '<br>')
	content = html_template.replace('[TITLE]', subject).replace('[CONTENT]', content)

	msg = MIMEText(content, 'html')
	msg['Subject'] = subject
	msg['From'] = f"{CONFIG['senders-name']} <{CONFIG['email-address']}>"
	msg['To'] = receiver

	content = msg.as_string()

	# ----------------------------------------------

	# Send
	try:
		smtpserver.sendmail(CONFIG['email-address'], receiver, content)
		smtpserver.close()
		# print('Sent')
		return True
	except Exception as e:
		print(f"ERROR Couldn't be sent: {e}")
		return False

if __name__ == '__main__':
	message = f"""Hello"""
	send_email(receiver="jack@gmail.com",
				subject='Whats up?',
				content=message)

