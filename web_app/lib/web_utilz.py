#!/usr/bin/env python3
# coding=utf-8
'''
#-------------------------------------------------------------------------------
Project		: Jaas
Module		: web_util
Purpose   	: Utility module of web app (app.py)
Version		: 2.0.1 beta
Status 		: Development

Modified	:
Created   	:
Author		: Burak Tokman
Email 		: buraktokman@hotmail.com
Copyright 	: 2020, Bulrosa OU
Licence   	: EULA
			  Unauthorized copying of this file, via any medium is strictly prohibited
			  Proprietary and confidential
#-------------------------------------------------------------------------------
'''
import sys
import urllib.request
from pathlib import Path
from datetime import datetime
from colorama import Style
from bs4 import BeautifulSoup
sys.path.insert(0, str(Path(Path(__file__).parents[2] / 'lib')))	# LIB
import postgres
import logz

def timestamp():
	"""Returns current time in UTC (Coordinated Universal Time)
	"""
	now = datetime.utcnow()
	output = '%.2d:%.2d:%.2d' % ((now.hour + 3) % 24, now.minute, now.second)
	return output


def load_html(config, html_path, header_path, footer_path):
	"""Prepare HTML template for process. Add header and footer. Include version info.
	"""
	html_doc = ''
	with open(str(header_path), encoding='utf-8') as f:
		html_header = f.read()
	with open(str(html_path), encoding='utf-8') as f:
		html_doc = f.read()
	with open(str(footer_path), encoding='utf-8') as f:
		html_footer = f.read()
	# Add header & footer
	html_doc = html_doc.replace('[HTML_HEADER]', html_header)
	html_doc = html_doc.replace('[HTML_FOOTER]', html_footer)
	# Version
	html_doc = html_doc.replace('[APP_VERSION]', config['app-version'])
	# Return
	return html_doc

def main():
	pass

if __name__ == '__main__':
	main()
