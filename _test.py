#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
#-------------------------------------------------------------------------------
Project		: Project JaaS
Module		: test
Purpose   	:
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
from halo import Halo
from bs4 import BeautifulSoup
from datetime import datetime
import time, os
import subprocess
import sys
import time
import threading
import random
import lorem
import names

def main():
	now = datetime.utcnow()
	# output = '%.2d:%.2d:%.2d' % ((now.hour + 3) % 24, now.minute, now.second)
	output = f"{now.strftime('%Y-%m-%d %H:%M:%S.%f')}"
	# Return
	print(output)

	time_update = '2020-03-05 16:09:30'
	time_now = '2020-04-15 16:09:30'

	time_update_unix = int(time.mktime(datetime.strptime(time_update, "%Y-%m-%d %H:%M:%S").timetuple()))
	time_now_unix = int(time.mktime(datetime.strptime(time_now, "%Y-%m-%d %H:%M:%S").timetuple()))
	print(time_update_unix)
	print(time_now_unix)

	s = datetime.utcfromtimestamp(int(time.time())).strftime('%H:%M:%S')
	print(s)


if __name__ == '__main__':
	main()