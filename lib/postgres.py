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

import sys
import time
import ast
import psycopg2
import base64
from datetime import datetime
from pathlib import Path
from colorama import Fore, Back, Style
sys.path.insert(0, str(Path(Path(__file__).parents[0])))
import logz


# [ ------------- CONFIGURATION ------------------ ]

CONFIG = {'dbname': 'jaas_dev',
			#'user': '',
			#'password': '',
			'host': '127.0.0.1'}

# [ ---------------------------------------------- ]

	#	#	#	#	#	#	#	#	#	#	#
	#										#
	#			CONNECTION 			 		#
	#										#
	#	#	#	#	#	#	#	#	#	#	#

def connect_db():
	"""Establish connection w/ postgres database
	"""
	global CONN, CONFIG
	# dns = f"dbname={CONFIG['dbname']} user={CONFIG['user']} password={CONFIG['password']} host={CONFIG['host']}"
	dns = f"dbname={CONFIG['dbname']} host={CONFIG['host']}"
	try:
		CONN = psycopg2.connect(dns)
		CONN.autocommit = True
		print(f"{logz.timestamp()}{Back.BLUE}{Fore.BLACK} POSTGRES → {Style.RESET_ALL}Connection established w/ database")
		return True
	except Exception as e:
		print(f"{logz.timestamp()}{Style.BRIGHT} POSTGRES → ERROR → Cannot connect to database")
		print(f"{Style.BRIGHT}{e}")
		return False

def disconnect_db():
	"""Close connection w/ database
	"""
	global CONN
	try:
		CONN.close()
		print(f"{logz.timestamp()}{Back.BLUE}{Fore.BLACK} POSTGRES → {Style.RESET_ALL}Database connection closed")
		return True
	except Exception as e:
		print(f"{logz.timestamp()}{Style.BRIGHT} POSTGRES → ERROR → Cannot disconnect from database")
		print(f"{Style.BRIGHT}{e}")
		return False


# [ ---------------------------------------------- ]

	#	#	#	#	#	#	#	#	#	#	#
	#										#
	#			USERS 				 		#
	#										#
	#	#	#	#	#	#	#	#	#	#	#

#	ADD --- --- --- --- --- ---

def add_user(time_add, email, full_name, time_zone, membership_status, membership_time_end):
	"""Add shipping option to product
	"""
	global CONN
	try:
		# Default Values
		if time_add == None:
			now = datetime.utcnow()
			time_add = now.strftime('%Y-%m-%d %H:%M:%S')
		# Time Zone
		if isinstance(time_zone, str):
			time_zone = '\'' + str(time_zone) + '\''
		else:
			time_zone = 'NULL'
		# Membership Status
		if membership_status == None:
			membership_status = True
		# Time End
		if isinstance(membership_time_end, str):
			membership_time_end = '\'' + str(membership_time_end) + '\''
		else:
			membership_time_end = 'NULL'
		# Format Content
		full_name = full_name.replace('"', '\'').replace("'", "''")
		temp = '\'' + str(time_add) + '\',\'' + str(email) + '\',\'' + str(full_name) + '\',' + str(time_zone) + ',' + str(membership_status) + ',' + str(membership_time_end)
		sql = 'INSERT INTO users (time_add, email, full_name, time_zone, membership_status, membership_time_end) VALUES (' + temp + ') RETURNING id;'
		cur = CONN.cursor()
		cur.execute(sql)
		output = cur.fetchone()
		cur.close()
		return output[0]
	except Exception as e:
		print(f'{logz.timestamp()}{Style.BRIGHT} POSTGRES → ERROR → Could not add user')
		print(Style.BRIGHT + str(sql))
		print(f"{Style.BRIGHT}{e}")
		return False

#	GET --- --- --- --- --- ---

def get_user(user_id):
	"""Fetch Joke by ID
	"""
	global CONN
	try:
		sql = 'SELECT * FROM users WHERE id=' + str(user_id)
		cur = CONN.cursor()
		cur.execute(sql)
		output = cur.fetchone()
		cur.close()
		# Modify Content
		# content = output[5].replace('\'', "'")
		content = output[5]
		# Create dict
		dict_temp = {
			'id' : output[0],
			'time_add' : output[1],
			'email' : output[2],
			'full_name' : output[3],
			'time_zone' : output[4],
			'membership_status' : content,
			'membership_time_end' : output[6]
			}
		return dict_temp
	except Exception as e:
		print(f'{logz.timestamp()}{Style.BRIGHT}POSTGRES → ERROR → Cannot fetch user id={user_id}')
		print(f"{Style.BRIGHT}{e}")
		return False

def get_user_all():
	"""
	"""
	global CONN
	try:
		sql = 'SELECT * FROM users ORDER BY time_add DESC NULLS LAST'
		cur = CONN.cursor()
		cur.execute(sql)
		outputs = cur.fetchall()
		cur.close()
		result = []
		for output in outputs:
			# Modify Content
			# content = output[5].replace('\'', "'")
			content = output[5]
			# Create dict
			dict_temp = {
				'id' : output[0],
				'time_add' : output[1],
				'email' : output[2],
				'full_name' : output[3],
				'time_zone' : output[4],
				'membership_status' : content,
				'membership_time_end' : output[6]
				}
			result.append(dict_temp)
		return result
	except Exception as e:
		print(f'{logz.timestamp()}{Style.BRIGHT}POSTGRES → ERROR → Cannot fetch all users')
		print(f"{Style.BRIGHT}{e}")
		return False

#	SET --- --- --- --- --- ---

def set_user_membership_time_end(user_id, time_end):
	"""
	"""
	global CONN
	try:
		sql = 'UPDATE users SET membership_time_end=\'' + str(time_end) + '\' WHERE id=' + str(user_id)
		cur = CONN.cursor()
		cur.execute(sql)
		cur.close()
		return True
	except Exception as e:
		print(logz.timestamp() + Style.BRIGHT + ' POSTGRES → ERROR → Could not set membership_time_end=' +str(time_end)+' for user='+str(user_id))
		# print(Style.BRIGHT + str(sql))
		print(f"{Style.BRIGHT}{e}")
		return False

def set_user_membership_status(user_id, status):
	"""
	"""
	global CONN
	try:
		sql = 'UPDATE users SET membership_status=' + str(status) + ' WHERE id=' + str(user_id)
		cur = CONN.cursor()
		cur.execute(sql)
		cur.close()
		return True
	except Exception as e:
		print(logz.timestamp() + Style.BRIGHT + ' POSTGRES → ERROR → Could not set membership_status=' +str(status)+' for user='+str(user_id))
		# print(Style.BRIGHT + str(sql))
		print(f"{Style.BRIGHT}{e}")
		return False

#	DEL --- --- --- --- --- ---

def del_user(user_id):
	"""Remove joke
	"""
	global CONN
	try:
		sql = 'DELETE FROM users WHERE id=' + str(user_id)
		cur = CONN.cursor()
		cur.execute(sql)
		cur.close()
		return True
	except Exception as e:
		print(logz.timestamp() + Style.BRIGHT + ' POSTGRES → ERROR → Could not remove user=' + str(user_id))
		print(f"{Style.BRIGHT}{e}")
		return False

# [ ---------------------------------------------- ]

	#	#	#	#	#	#	#	#	#	#	#
	#										#
	#			JOKES 				 		#
	#										#
	#	#	#	#	#	#	#	#	#	#	#

#	ADD --- --- --- --- --- ---

def add_joke(time_add, time_add_original, url, author, title, content, rating, comment_count, vote_count, language, shared_on_twitter, flair):
	"""Add shipping option to product
	"""
	global CONN
	try:
		# Default Values
		now = datetime.utcnow()
		if time_add == None:
			time_add = now.strftime('%Y-%m-%d %H:%M:%S')
		if time_add_original == None:
			time_add_original = now.strftime('%Y-%m-%d %H:%M:%S')
		if language == None:
			language = 'eng'
		if shared_on_twitter == None or shared_on_twitter == False:
			shared_on_twitter = 'NULL'
		else:
			shared_on_twitter = '\'' + str(shared_on_twitter) + '\''
		if flair == None:
			flair = 'NULL'
		else:
			flair = '\'' + str(flair) + '\''
		if rating == None:			rating = 'NULL'
		if vote_count == None:		vote_count = 'NULL'
		if comment_count == None:	comment_count = 'NULL'
		# Format Content
		content = content.replace('‘','\'').replace("'", "''")#.replace('“', '"').replace('"', '""')
		title = title.replace('"', '\'').replace("'", "''")
		temp = '\'' + str(time_add) + '\',\'' + str(time_add_original) + '\',\'' + str(url) + '\',\'' + str(author) + '\',\'' + str(title) + '\',\'' + str(content) + '\',' + str(rating) + ',' + str(comment_count) + ',' + str(vote_count) + ',\'' + str(language) + '\',' + str(shared_on_twitter) + ',' + str(flair)
		sql = 'INSERT INTO jokes (time_add, time_add_original, url, author, title, content, rating, comment_count, vote_count, language, shared_on_twitter, flair) VALUES (' + temp + ') RETURNING id;'
		cur = CONN.cursor()
		cur.execute(sql)
		output = cur.fetchone()
		cur.close()
		return output[0]
	except Exception as e:
		print(f'{logz.timestamp()}{Style.BRIGHT} POSTGRES → ERROR → Could not add joke\ntime_add={time_add} time_add_original={time_add_original} url={url} author={author} content={content} rating={rating} comment_count={comment_count} vote_count={vote_count} language={language} shared_on_twitter={shared_on_twitter} flair={flair}')
		# print(Style.BRIGHT + str(sql))
		print(f"{Style.BRIGHT}{e}")
		return False

#	GET --- --- --- --- --- ---

def get_joke_all():
	"""Fetch Joke by ID
	"""
	global CONN
	try:
		sql = 'SELECT * FROM jokes ORDER BY time_add_original DESC NULLS LAST'
		cur = CONN.cursor()
		cur.execute(sql)
		outputs = cur.fetchall()
		cur.close()
		result = []
		for output in outputs:
			# Modify Content
			# content = output[5].replace('\'', "'")
			content = output[5]#.rstrip().lstrip()
			# Create dict
			dict_temp = {
				'id' : output[0],
				'time_add' : output[1],
				'time_add_original' : output[2],
				'time_update' : output[13],
				'url' : output[3],
				'author' : output[4],
				'title' : output[12],
				'content' : content,
				'rating' : output[6],
				'comment_count' : output[7],
				'vote_count' : output[8],
				'language' : output[9],
				'shared_on_twitter' : output[10],
				'flair' : output[11],
				}
			result.append(dict_temp)
		return result
	except Exception as e:
		print(f'{logz.timestamp()}{Style.BRIGHT}POSTGRES → ERROR → Cannot fetch all jokes')
		print(f"{Style.BRIGHT}{e}")
		return False

def get_joke_all_filtered():
	"""Fetch Joke by ID
	"""
	global CONN
	try:
		sql = 'SELECT * FROM jokes WHERE Length(content) > 600 AND jokes.comment_count > 100 ORDER BY comment_count DESC NULLS LAST '
		cur = CONN.cursor()
		cur.execute(sql)
		outputs = cur.fetchall()
		cur.close()
		result = []
		for output in outputs:
			# Modify Content
			# content = output[5].replace('\'', "'")
			content = output[5]#.rstrip().lstrip()
			# Create dict
			dict_temp = {
				'id' : output[0],
				'time_add' : output[1],
				'time_add_original' : output[2],
				'time_update' : output[13],
				'url' : output[3],
				'author' : output[4],
				'title' : output[12],
				'content' : content,
				'rating' : output[6],
				'comment_count' : output[7],
				'vote_count' : output[8],
				'language' : output[9],
				'shared_on_twitter' : output[10],
				'flair' : output[11],
				}
			result.append(dict_temp)
		return result
	except Exception as e:
		print(f'{logz.timestamp()}{Style.BRIGHT}POSTGRES → ERROR → Cannot fetch all jokes filtered')
		print(f"{Style.BRIGHT}{e}")
		return False

def get_joke(joke_id):
	"""Fetch Joke by ID
	"""
	global CONN
	try:
		sql = 'SELECT * FROM jokes WHERE id=' + str(joke_id)
		cur = CONN.cursor()
		cur.execute(sql)
		output = cur.fetchone()
		cur.close()
		# Modify Content
		# content = output[5].replace('\'', "'")
		content = output[5]
		# Create dict
		dict_temp = {
			'id' : output[0],
			'time_add' : output[1],
			'time_add_original' : output[2],
			'time_update' : output[13],
			'url' : output[3],
			'author' : output[4],
			'title' : output[12],
			'content' : content,
			'rating' : output[6],
			'comment_count' : output[7],
			'vote_count' : output[8],
			'language' : output[9],
			'shared_on_twitter' : output[10],
			'flair' : output[11],
			}
		return dict_temp
	except Exception as e:
		print(f'{logz.timestamp()}{Style.BRIGHT}POSTGRES → ERROR → Cannot fetch joke id={joke_id}')
		print(f"{Style.BRIGHT}{e}")
		return False

def get_joke_by_url(url):
	"""Fetch Joke by ID
	"""
	global CONN
	try:
		# Trim URL
		# url = 'https://www.reddit.com/r/Jokes/comments/77g7ub/a_woman_goes_to_buy_a_parrot_the_prices_are_100/
		if 'comments/' in url:
			url = url.split('comments/')[1]
		# SQL
		sql = '''SELECT id FROM jokes
					WHERE url ILIKE '%''' + str(url) + '''%'
					ORDER BY time_add_original
					DESC NULLS LAST;'''
		cur = CONN.cursor()
		cur.execute(sql)
		output = cur.fetchone()
		cur.close()
		dict_temp = get_joke(joke_id=output[0])
		return dict_temp
	except Exception as e:
		# print(f'{logz.timestamp()}{Style.BRIGHT}POSTGRES → ERROR → While finding joke by URL\n{url}')
		# print(f"{Style.BRIGHT}{e}")
		return False

#	SET --- --- --- --- --- ---

def set_joke_rating(joke_id, rating):
	"""
	"""
	global CONN
	try:
		if rating == None:
			rating = 'NULL'
		sql = 'UPDATE jokes SET rating=' + str(rating) + ' WHERE id=' + str(joke_id)
		cur = CONN.cursor()
		cur.execute(sql)
		cur.close()
		return True
	except Exception as e:
		print(logz.timestamp() + Style.BRIGHT + ' POSTGRES → ERROR → Could not set rating=' +str(rating)+' for joke='+str(joke_id))
		# print(Style.BRIGHT + str(sql))
		print(f"{Style.BRIGHT}{e}")
		return False

def set_joke_comment_count(joke_id, comment_count):
	"""
	"""
	global CONN
	try:
		if comment_count == None:
			comment_count = 'NULL'
		sql = 'UPDATE jokes SET comment_count=' + str(comment_count) + ' WHERE id=' + str(joke_id)
		cur = CONN.cursor()
		cur.execute(sql)
		cur.close()
		return True
	except Exception as e:
		print(logz.timestamp() + Style.BRIGHT + ' POSTGRES → ERROR → Could not set comment_count=' +str(comment_count)+' for joke='+str(joke_id))
		# print(Style.BRIGHT + str(sql))
		print(f"{Style.BRIGHT}{e}")
		return False

def set_joke_vote_count(joke_id, vote_count):
	"""
	"""
	global CONN
	try:
		if vote_count == None:
			vote_count = 'NULL'
		sql = 'UPDATE jokes SET vote_count=' + str(vote_count) + ' WHERE id=' + str(joke_id)
		cur = CONN.cursor()
		cur.execute(sql)
		cur.close()
		return True
	except Exception as e:
		print(logz.timestamp() + Style.BRIGHT + ' POSTGRES → ERROR → Could not set vote count=' +str(vote_count)+' for joke='+str(joke_id))
		# print(Style.BRIGHT + str(sql))
		print(f"{Style.BRIGHT}{e}")
		return False

def set_joke_shared_on_twitter(joke_id, time_shared):
	"""
	"""
	global CONN
	try:
		# Default Values
		if time_shared == None:
			now = datetime.utcnow()
			time_shared = now.strftime('%Y-%m-%d %H:%M:%S')
		sql = 'UPDATE jokes SET shared_on_twitter=\'' + str(time_shared) + '\' WHERE id=' + str(joke_id)
		cur = CONN.cursor()
		cur.execute(sql)
		cur.close()
		return True
	except Exception as e:
		print(logz.timestamp() + Style.BRIGHT + ' POSTGRES → ERROR → Could not set shared on twitter joke=' + str(joke_id) + ' shared=' + str(time_shared))
		# print(Style.BRIGHT + str(sql))
		print(f"{Style.BRIGHT}{e}")
		return False

def set_joke_tweet_url(joke_id, tweet_url):
	"""
	"""
	global CONN
	try:
		sql = 'UPDATE jokes SET tweet_url=\'' + str(tweet_url) + '\' WHERE id=' + str(joke_id)
		cur = CONN.cursor()
		cur.execute(sql)
		cur.close()
		return True
	except Exception as e:
		print(logz.timestamp() + Style.BRIGHT + ' POSTGRES → ERROR → Could not set tweet url=' +str(tweet_url)+' for joke='+str(joke_id))
		# print(Style.BRIGHT + str(sql))
		print(f"{Style.BRIGHT}{e}")
		return False

def set_joke_time_update(joke_id, time_update):
	"""
	"""
	global CONN
	try:
		# Default Values
		if time_update == None:
			now = datetime.utcnow()
			time_update = now.strftime('%Y-%m-%d %H:%M:%S')
		sql = 'UPDATE jokes SET time_update=\'' + str(time_update) + '\' WHERE id=' + str(joke_id)
		cur = CONN.cursor()
		cur.execute(sql)
		cur.close()
		return True
	except Exception as e:
		print(logz.timestamp() + Style.BRIGHT + ' POSTGRES → ERROR → Could not update time for joke=' + str(joke_id) + ' shared=' + str(time_update))
		# print(Style.BRIGHT + str(sql))
		print(f"{Style.BRIGHT}{e}")
		return False

#	DEL --- --- --- --- --- ---

def del_joke(joke_id):
	"""Remove joke
	"""
	global CONN
	try:
		sql = 'DELETE FROM jokes WHERE id=' + str(joke_id)
		cur = CONN.cursor()
		cur.execute(sql)
		cur.close()
		return True
	except Exception as e:
		print(logz.timestamp() + Style.BRIGHT + ' POSTGRES → ERROR → Could not remove joke=' + str(joke_id))
		print(f"{Style.BRIGHT}{e}")
		return False

# [ ---------------------------------------------- ]

	#	#	#	#	#	#	#	#	#	#	#
	#										#
	#			JOKE SEND 				 	#
	#										#
	#	#	#	#	#	#	#	#	#	#	#

#	ADD --- --- --- --- --- ---

def add_joke_send(joke_id, user_id, time_send):
	"""
	"""
	global CONN
	try:
		# Default Values
		if time_send == None:
			now = datetime.utcnow()
			time_send = now.strftime('%Y-%m-%d %H:%M:%S')
		# Create SQL
		temp = str(joke_id) + ',' + str(user_id) + ',\'' + str(time_send) + '\''
		sql = 'INSERT INTO jokes_send (joke_id, user_id, time_send) VALUES (' + temp + ') RETURNING id;'
		cur = CONN.cursor()
		cur.execute(sql)
		output = cur.fetchone()
		cur.close()
		return output[0]
	except Exception as e:
		print(f'{logz.timestamp()}{Style.BRIGHT} POSTGRES → ERROR → Could not add jokes to sent')
		print(Style.BRIGHT + str(sql))
		print(f"{Style.BRIGHT}{e}")
		return False

#	GET --- --- --- --- --- ---

def did_joke_send_before(joke_id, user_id):
	"""Fetch Joke by ID
	"""
	global CONN
	try:
		sql = 'SELECT * FROM jokes_send WHERE joke_id=' + str(joke_id) + ' AND user_id=' + str(user_id)
		cur = CONN.cursor()
		cur.execute(sql)
		output = cur.fetchone()
		cur.close()
		if output == None:
			return None
		else:
			dict_temp = {
				'id' : output[0],
				'joke_id' : output[1],
				'user_id' : output[2],
				'time_send' : output[3]
				}
			return dict_temp
	except Exception as e:
		print(f'{logz.timestamp()}{Style.BRIGHT}POSTGRES → ERROR → Cannot fetch joke if joke sent before. user id={user_id}' + ' joke_id=' + str(joke_id))
		print(f"{Style.BRIGHT}{e}")
		return False

#	SET --- --- --- --- --- ---

#	DEL --- --- --- --- --- ---

def del_joke_send_all(joke_id):
	"""Remove joke
	"""
	global CONN
	try:
		sql = 'DELETE FROM jokes_send WHERE joke_id=' + str(joke_id)
		cur = CONN.cursor()
		cur.execute(sql)
		cur.close()
		return True
	except Exception as e:
		print(logz.timestamp() + Style.BRIGHT + ' POSTGRES → ERROR → Could not joke send user . joke_id=' + str(joke_id))
		print(f"{Style.BRIGHT}{e}")
		return False

# [ ---------------------------------------------- ]

	#	#	#	#	#	#	#	#	#	#	#
	#										#
	#			JOKES 				 		#
	#										#
	#	#	#	#	#	#	#	#	#	#	#

#	ADD --- --- --- --- --- ---

def add_joke_comment(joke_id, time_add, url, author, content, vote_count, lang):
	"""Add shipping option to product
	"""
	global CONN
	try:
		# Default Values
		if time_add == None:
			now = datetime.utcnow()
			time_add = now.strftime('%Y-%m-%d %H:%M:%S')
		if lang == None:
			lang = 'NULL'
		# Format Content
		content = content.replace('"', '\'').replace("'", "''")
		temp = str(joke_id) + ',\'' + str(time_add) + '\',\'' + str(url) + '\',\'' + str(author) + '\',\'' + str(content) + '\',' + str(vote_count) + ',' + str(lang)
		sql = 'INSERT INTO jokes_comments (joke_id, time_add, url, author, content, vote_count, lang) VALUES (' + temp + ') RETURNING id;'
		cur = CONN.cursor()
		cur.execute(sql)
		output = cur.fetchone()
		cur.close()
		return output[0]
	except Exception as e:
		print(f'{logz.timestamp()}{Style.BRIGHT} POSTGRES → ERROR → Could not add comment to joke={joke_id}')
		print(Style.BRIGHT + str(sql))
		print(f"{Style.BRIGHT}{e}")
		return False

#	GET --- --- --- --- --- ---

def get_joke_comments(joke_id):
	"""Fetch Joke by ID
	"""
	global CONN
	try:
		sql = 'SELECT * FROM jokes_comments WHERE joke_id=' + str(joke_id) + ' ORDER BY time_add_original DESC NULLS LAST'
		cur = CONN.cursor()
		cur.execute(sql)
		outputs = cur.fetchall()
		cur.close()
		result = []
		for output in outputs:
			# Modify Content
			# content = output[5].replace('\'', "'")
			content = output[5]
			# Create dict
			dict_temp = {
				'id' : output[0],
				'joke_id' : output[1],
				'time_add' : output[2],
				'url' : output[3],
				'author' : output[4],
				'content' : content,
				'vote_count' : output[6],
				'language' : output[7]
				}
			result.append(dict_temp)
		return result
	except Exception as e:
		print(f'{logz.timestamp()}{Style.BRIGHT}POSTGRES → ERROR → Cannot fetch joke id={joke_id}')
		print(f"{Style.BRIGHT}{e}")
		return False

#	SET --- --- --- --- --- ---

def set_joke_comment_time_update(comment_id, time_update):
	"""
	"""
	global CONN
	try:
		# Default Values
		if time_update == None:
			now = datetime.utcnow()
			time_update = now.strftime('%Y-%m-%d %H:%M:%S')
		sql = 'UPDATE jokes_comments SET time_update=\'' + str(time_update) + '\' WHERE id=' + str(comment_id)
		cur = CONN.cursor()
		cur.execute(sql)
		cur.close()
		return True
	except Exception as e:
		print(logz.timestamp() + Style.BRIGHT + ' POSTGRES → ERROR → Could not update time for joke comment=' + str(joke_id) + ' shared=' + str(time_update))
		# print(Style.BRIGHT + str(sql))
		print(f"{Style.BRIGHT}{e}")
		return False

#	DEL --- --- --- --- --- ---

def del_joke_comment(comment_id):
	"""
	"""
	global CONN
	try:
		sql = 'DELETE FROM jokes_comments WHERE id=' + str(comment_id)
		cur = CONN.cursor()
		cur.execute(sql)
		cur.close()
		return True
	except Exception as e:
		print(logz.timestamp() + Style.BRIGHT + ' POSTGRES → ERROR → Could not remove joke comment_id=' + str(comment_id))
		print(f"{Style.BRIGHT}{e}")
		return False

def del_joke_comment_all(joke_id):
	"""
	"""
	global CONN
	try:
		sql = 'DELETE FROM jokes_comments WHERE joke_id=' + str(joke_id)
		cur = CONN.cursor()
		cur.execute(sql)
		cur.close()
		return True
	except Exception as e:
		print(logz.timestamp() + Style.BRIGHT + ' POSTGRES → ERROR → Could not remove comments of the joke_id=' + str(joke_id))
		print(f"{Style.BRIGHT}{e}")
		return False


# [ ---------------------------------------------- ]

	#	#	#	#	#	#	#	#	#	#	#
	#										#
	#			CUSTOM 						#
	#										#
	#	#	#	#	#	#	#	#	#	#	#

def main():
	r = connect_db()

# 	r = add_joke(time_add=None,
# 					time_add_original='2017-03-16 11:48:33',
# 					url='https://www.reddit.com/r/Jokes/comments/77g7ub/a_woman_goes_to_buy_a_parrot_the_prices_are_100/',
# 					author='test12',
# 					content='''"Because he used to live in a brothel" says the shopkeeper. She pays $15!"''',
# 					rating=0.88,
# 					comment_count=9564,
# 					vote_count=485050,
# 					language=None,
# 					shared_on_twitter=False,
# 					flair='nsfw')

	# r = get_joke(r=121478)
	r = get_joke_all_filtered()
	print(len(r))
	# r = add_user(time_add='2019-03-04 09:09:50',
	# 			email='bo@lve.com',
	# 			full_name='tes test',
	# 			time_zone=None,
	# 			membership_status=True,
	# 			membership_time_end=None)

	# r =  add_joke_send(joke_id=6, user_id=1, time_send=None)

	# r = did_joke_send_before(joke_id=121103, user_id=1)
	# print(r)
	# r = del_joke_send_all(joke_id=6)

	# r = add_joke_comment(joke_id=6,
	# 					time_add=None,
	# 					url='https://www.reddit.com/r/Jokes/comments/77g7ub/a_woman_goes_to_buy_a_parrot_the_prices_are_100/dolsjue?utm_source=share&utm_medium=web2x',
	# 					author='121_sbdias',
	# 					content='''I'll tell you what's wrong with it, my lad. He's dead, that's what's wrong with it!''',
	# 					vote_count=564,
	# 					lang=None)

	# r = set_joke_tweet_url(joke_id=26714, tweet_url='https://t.co/YfXJGPSAZw')

	disconnect_db()

if __name__ == '__main__':
	main()