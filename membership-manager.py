#! usr/bin/env python3
# -*- coding: utf-8 -*-
'''
#-------------------------------------------------------------------------------
Project		: Project JaaS
Module		: membership_manager
Purpose   	: Add new users & check membership status of existing ones
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

CONFIG = {'refresh-interval': 10 # mins
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
    # Connect to DB
    postgres.connect_db()

    while True:
        # Start
        time_start = time.time()

        # ------ FETCH USERS ---------------------------

        print(f"{logz.timestamp()}{Fore.GREEN} MEMBERSHIP → INIT → {Style.RESET_ALL}Fething users...")
        # From database
        users_database = postgres.get_user_all()
        # From Shopify (or ?)

        # ----------------------------------------------

            #   #   #   #   #   #   #   #   #   #   #
            #                                       #
            #           MANAGE                      #
            #                                       #
            #   #   #   #   #   #   #   #   #   #   #

        # ------ OLD USERS -----------------------------

        print(f"{logz.timestamp()}{Fore.GREEN} MEMBERSHIP → EXISTING → {Style.RESET_ALL}Checking expired memberships")
        for user in users_database:
            # Check if membership of existing users
            if check_membership_status(user) == False:
                print(f"{logz.timestamp()}{Fore.GREEN} MEMBERSHIP → CAUTION → {Style.RESET_ALL}User {user['id']} membership expired")
                r = postgres.set_user_membership_status(user_id=user['id'],
                                                        status=False)

        # ------ NEW USERS -----------------------------

        #
        #   INCOMPLETE - FETCH FROM WHERE?
        #
        # users_remote = shopify.get_orders()

        # for user in users_remote:
        #     for user_local in users_database:
        #         if user_local['email'] == user['email']:
        #             # Add user to database

        #             # Send Welcome joke

        #             # Mark joke as sent

        #             break


        # ------ SLEEP ---------------------------------

        print(f"{logz.timestamp()}{Fore.GREEN} MEMBERSHIP → COMPLETED → {Style.RESET_ALL}Sleeping {CONFIG['refresh-interval'] * 60}mins")
        time.sleep(CONFIG['refresh-interval'] * 60)



if __name__ == '__main__':
	main()
