#!/usr/bin/env python3
# coding=utf-8
'''
#-------------------------------------------------------------------------------
Project		: Jaas - Joke as a Service, Web App
Module		: app
Purpose   	: Initiate Web UI for Davalos DS
Version		: 0.7.1 beta
Status 		: Development

Modified	: 2020 Jul 20
Created   	: 2020 Jul 20
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
import socket
# import psutil
# import filetype
# import phonenumbers
import os
from pathlib import Path
from math import ceil
from colorama import Fore, Back, Style
from operator import itemgetter
from datetime import datetime
from random import randrange
from flask import Flask, render_template_string, request, redirect, url_for, make_response, session
# from flask_login import LoginManager, current_user, login_user, logout_user, login_required, UserMixin
from lib import web_utilz
sys.path.insert(0, str(Path(Path(os.path.abspath(__file__)).parents[1] / 'lib')))	# LIB
import postgres
import logz

# [ ------------- CONFIGURATION ------------------ ]
#
#	INCOMPLETE - FETCH DYNAMICALY FROM DB ?
#
CONFIG = {	'app-version' : '2.0.1',
			'database-ip' : '0.0.0.0',
			'database-port' : 5432,
			'html-dir' : Path(Path(__file__).parents[0] / 'templates')}


# [ ---------------------------------------------- ]

# Connect to DB
postgres.connect_db()

# Flask Configuration
app = Flask(__name__, static_folder='/static')
app._static_folder = str(Path(Path(__file__).parents[0] / 'static'))
app.config['SECRET_KEY'] = "" # Secret key for your app


# [ ---------------------------------------------- ]

	#	#	#	#	#	#	#	#	#	#	#
	#										#
	#			HOME 			 			#
	#										#
	#	#	#	#	#	#	#	#	#	#	#


@app.route('/', methods=['GET'])
def single():
	"""
		Home page of Davalos DS
	"""
	global CONFIG

	# ------------- PREPARE ------------------------

	# Start timer
	time_page_start = time.time()

	# Read HTML template
	html_doc = web_utilz.load_html(config=CONFIG,
								html_path=CONFIG['html-dir'] / 'single.html',
								header_path=CONFIG['html-dir'] / 'header.html',
								footer_path=CONFIG['html-dir'] / 'footer.html')

	# Params
	j_id = request.args.get('id', default = None, type = int)

	# ----------------------------------------------

		#	#	#	#	#	#	#	#	#	#	#
		#										#
		#			JOKE 						#
		#										#
		#	#	#	#	#	#	#	#	#	#	#

	# Fetch
	joke = None
	while not joke:
		if j_id is None or joke is False:
			print('selecting random joke...')
			j_id = randrange(444331)
		joke =  postgres.get_joke(joke_id=j_id)

	print(f"{logz.timestamp()}{Fore.YELLOW} WEB-APP → SINGLE → {Style.RESET_ALL}Joke id={j_id}")

	# ------------- EDIT HTML ----------------------

	# Title & Content
	if len(joke['title']) >= 54:
		title = f"{joke['title'][:54]}..."
		content = joke['title'] + '\n ' + joke['content']
	else:
		title = joke['title']
		content = joke['content'] # joke['title'] + '\n ' + joke['content']
	content = content.replace('\n', '</br>')
	html_doc = html_doc.replace('[CONTENT]', content)
	# '<p class="if ig as ih b eq ii ij et ik il im in ey io ip fb iq ir fe is di eo">[CONTENT]</p>'

	# URL Next Joke
	url_next = f"/?id={joke['id'] + 1}"
	author = joke['author']
	url = joke['url']
	joke_id = joke['id']
	comment_count = joke['comment_count']
	vote_count = joke['vote_count']
	rating = joke['rating']
	flair = joke['flair']
	time_add_original = joke['time_add_original']
	time_update = joke['time_update']

	# total_revenue_30day = '$' + "{0:,.2f}".format(counter['revenue_30day'])

	# Trim Title
	#f"🤩 {joke['title']}"

	# Add timer
	time_load = str(round(time.time() - time_page_start, 2)) + ' secs'
	print(f"{logz.timestamp()}{Fore.YELLOW} WEB-APP → SINGLE → {Style.RESET_ALL}Page rendered in {time_load}")
	# Return
	return render_template_string(html_doc, **locals())



# [ ---------------------------------------------- ]

	#	#	#	#	#	#	#	#	#	#	#
	#										#
	#			PRODUCT DESCRIPTION 	 	#
	#										#
	#	#	#	#	#	#	#	#	#	#	#

@app.route('/product/desc', methods=['GET'])
def product_description():
	"""
		Show only item's description
	"""

	# ------------- PREPARE ------------------------

	# Start timer
	time_page_start = time.time()
	# Arguments
	args = {'product-id' : request.args.get('id', default = None, type = int),}

	# ------------- DOWNLOAD -----------------------
	try:
		r = product_get.main(product_id=args['product-id'], category=False, images=False, merchant=False,
							identifier=True, description=True, package=False,
							attributes=False, features=False, rating=False, shipping=False)['description']
		# Read CSS from style.css to variable for description
		with open(str(Path(Path(__file__).parents[0] / 'static' / 'css' / 'davalos-prod-desc.css'))) as f:
			css = f.read()
		r = f"<style>{css}</style>{r}"
	except Exception as e:
		print(f"{Style.BRIGHT}{logz.timestamp()} WEB-APP → PRODUCT → DESCRIPTION → ERROR → {e}")
		r = 'N/A'

	# ------------- RETURN -------------------------
	time_load = str(round(time.time() - time_page_start, 2)) + ' secs'
	print(f"{logz.timestamp()}{Fore.YELLOW} WEB-APP → PRODUCT → DESCRIPTION → {Style.RESET_ALL}Page rendered in {time_load}")
	# Return
	return render_template_string(r)

# [ ---------------------------------------------- ]

	#	#	#	#	#	#	#	#	#	#	#
	#										#
	#			SET PROD. IDENTIFIER 	 	#
	#										#
	#	#	#	#	#	#	#	#	#	#	#

@app.route('/product/set/identifier', methods=['GET', 'POST'])
def set_product_identifier():
	"""
		Select identifier type then add/update id value
	"""
	global CONFIG

	# ------------- PREPARE ------------------------

	# Start timer
	time_page_start = time.time()
	if request.method == 'POST':
		args = {'id' : request.form['id'],
				'type' : request.form['type'],
				'value' : request.form['value']}
	else:
		# Arguments
		args = {'id' : request.args.get('id', default = None, type = int),
				'type' : request.args.get('type', default = None, type = str),
				'value' : None}

	# Prepare HTML
	html_doc = web_utilz.load_html(config=CONFIG,
									html_path=CONFIG['html-dir'] / 'product-set-identifier.html',
									header_path=CONFIG['html-dir'] / 'product-header.html',
									footer_path=CONFIG['html-dir'] / 'order-footer.html')

	# ------------- EDIT HTML ----------------------

	if args['id'] == None: args['id'] = ''
	if args['type'] == None: args['type'] = ''
	if args['value'] == None: args['value'] = ''
	product_id = args['id']
	html_doc = html_doc.replace('[VALUE]', str(args['value']))
	html_temp = ''
	# Insert to DB
	if args['value'] != None and args['type'] != '':
		try:
			r = postgres.set_product_identifier(product_id=args['id'],
												identifier_type=args['type'],
												value=args['value'])
			if r == True: html_temp = """<div id="DIV_7" style="margin: 10px 0px; 10px 0px;"><div id="DIV_8">  <div id="DIV_9">    <i id="I_10"></i>    <div id="DIV_11">      <span id="SPAN_12">Identifier updated</span>    </div>  </div></div></div>"""
			else: html_temp = """<div id="DIV_1" style="margin: 10px 0px; 10px 0px;"><div id="DIV_2">  <div id="DIV_3">    <i id="I_4"></i>    <div id="DIV_5">      <span id="SPAN_6">An error occurred when tried to update identifier</span>    </div>  </div></div></div>"""
		except Exception as e:
			print(f"{logz.timestamp()}{Style.BRIGHT} WEB-APP → ORDER → SET → ERROR → Cannot update product identifier")
			print(f"{Style.BRIGHT}{e}")
	else:
		html_temp = ''
	html_doc = html_doc.replace('[STATUS]', html_temp)

	# ------------- RETURN -------------------------

	time_load = str(round(time.time() - time_page_start, 2)) + ' secs'
	print(f"{logz.timestamp()}{Fore.YELLOW} WEB-APP → PRODUCT → SET → IDENTIFIER → {Style.RESET_ALL}Page rendered in {time_load}")
	# Return
	return render_template_string(html_doc, **locals())

# [ ---------------------------------------------- ]

	#	#	#	#	#	#	#	#	#	#	#
	#										#
	#			CATALOG 				 	#
	#										#
	#	#	#	#	#	#	#	#	#	#	#

@app.route('/catalog/', methods=['GET', 'POST'])
def catalog():
	"""
		List items in product catalog
	"""
	global CONFIG

	# ------------- PREPARE ------------------------

	# Start timer
	time_page_start = time.time()
	# Read HTML template
	html_doc = web_utilz.load_html(config=CONFIG,
								html_path=CONFIG['html-dir'] / 'catalog.html',
								header_path=CONFIG['html-dir'] / 'header.html',
								footer_path=CONFIG['html-dir'] / 'footer.html')

	# Arguments
	prod_per_page = request.args.get('per', default = 20, type = int)
	page_num_current = request.args.get('page', default = 1, type = int)
	search = request.args.get('search', default = None, type = str)

	# Searched or Not
	if request.method == 'POST':
		search = request.form['search']
		prod_ids_temp = postgres.get_product_id_by_title(request.form['search'])
	elif search != None: prod_ids_temp = postgres.get_product_id_by_title(search)
	# Get items in remote inventory
	else: prod_ids_temp = postgres.get_product_ids(platform=False, descending=True, updated_list=True)

	# Divide product ids for pages
	if len(prod_ids_temp) >= prod_per_page: products = [prod_ids_temp[x:x+prod_per_page] for x in range(0, len(prod_ids_temp), prod_per_page)]
	else: products = [prod_ids_temp]
	# Paging
	page_num_max = ceil(len(prod_ids_temp) / prod_per_page)
	if not len(prod_ids_temp) <= prod_per_page: products = [prod_ids_temp[x:x+prod_per_page] for x in range(0, len(prod_ids_temp), prod_per_page)]
	else: products = [prod_ids_temp]
	# If current page exceeds max
	if page_num_current > page_num_max: page_num_current = page_num_max

	# ------------- EDIT HTML ----------------------

	# Page Previous
	if page_num_current <= 1:
		html_doc = html_doc.replace('[PAGE_NUM_PREV_PLACEHOLDER]', '')
	else:
		html_page_prev = '''<span><li class="a-unselected"><a href="?page={{ page_num_prev }}&per={{ prod_per_page }}&search={{ search }}">{{ page_num_prev }}</a></li></span>'''
		html_doc = html_doc.replace('[PAGE_NUM_PREV_PLACEHOLDER]', html_page_prev)
	# Page Next
	if page_num_current >= page_num_max:
		html_doc = html_doc.replace('[PAGE_NUM_NEXT_PLACEHOLDER]', '')
	else:
		html_page_next = '''<span><li class="a-unselected"><a href="?page={{ page_num_next }}&per={{ prod_per_page }}&search={{ search }}">{{ page_num_next }}</a></li></span>'''
		html_doc = html_doc.replace('[PAGE_NUM_NEXT_PLACEHOLDER]', html_page_next)
	# Paging
	if search == None or search =='None': html_doc = html_doc.replace('&search={{ search }}', '')
	product_count = "{:,}".format(len(prod_ids_temp))
	page_num_prev = page_num_current - 1
	page_num_next = page_num_current + 1
	tr_all = ''

	# ----------------------------------------------

		#	#	#	#	#	#	#	#	#	#	#
		#										#
		#			LIST PRODUCTS 				#
		#										#
		#	#	#	#	#	#	#	#	#	#	#

	for prod_id in products[page_num_current - 1]:
		product_temp = product_get.main(product_id=prod_id, category=False, images=True,
								merchant=True, identifier=True, description=False, features=True,
								package=False, attributes=False, rating=True, shipping=True)
		if product_temp == False:
			print(f"{logz.timestamp()}{Style.BRIGHT} WEB-APP → CATALOG → ERROR → Product N/A. Skipping")
			continue
		tr_product = '''<tr class="mt-row">
						<td class="mt-cell mt-left"></td>
						<td class="mt-cell mt-center"><span class="a-declarative">
						  <div class="a-checkbox main-entry mt-row-select">
							<label>
							  <input type="checkbox" name="">
							  <i class="a-icon a-icon-checkbox"></i><span class="a-label a-checkbox-label"></span></label>
						  </div>
						  </span></td>
						<td class="mt-cell mt-left">[PRODUCT_ID]</td>
						<td class="mt-cell mt-left"><div class="mt-combination mt-layout-inline">
							<div >
							  <div class="mt-text mt-wrap-bw"><span class="mt-text-content mt-table-main">[STATUS]</span> </div>
							</div>
						  </div></td>
						<td class="mt-cell mt-center"><div class="myi-sprite-container myi-image">
							<div class="mt-text mt-center"><img alt="" style="max-height: 45px;" src="[IMAGE_URL]"></div>
							</div></td>
						<td class="mt-cell mt-left"><div class="mt-combination mt-layout-block">
							<div>
							  <div class="clamped wordbreak">
								<div class="mt-text mt-wrap-bw"> <span class="mt-text-content mt-table-main">[SKU]</span> </div>
							  </div>
							</div>
							<div>
							  <div class="mt-text mt-wrap-bw"> <span class="mt-text-content mt-table-detail">[CONDITION]</span> </div>
							</div>
						  </div></td>
						<td class="mt-cell mt-left"><div class="mt-combination mt-layout-block">
							<div>
							  <div class="mt-link mt-wrap-bw clamped wordbreak" title="[PRODUCT_TITLE]"><a class="a-link-normal mt-table-main" target="_blank" rel="noopener" href="/product?id=[PRODUCT_ID]">[PRODUCT_TITLE]</a></div>
							</div>
							<div>
							  <div class="mt-text mt-wrap-bw"> <span class="mt-text-content mt-table-detail"><a href="https://www.amazon.com/dp/[ASIN]" style="text-decoration: none; color: #666;" target="_blank">[ASIN]</a></span></div>
							</div>
						  </div></td>
						<td class="mt-cell mt-left"><div class="mt-combination mt-layout-block">
							<div>
							  <div class="mt-text mt-wrap-bw"> <span class="mt-text-content mt-table-main">[TIME_CREATION]</span></div>
							</div>
							<div>
							  <div class="mt-text mt-wrap-bw"> <span class="mt-text-content mt-table-detail">[TIME_UPDATE]</span></div>
							</div>
						  </div></td>
						<td class="mt-cell mt-right"><div class="mt-combination mt-layout-inline">
							<div>
							  <div class="mt-box">
								<label id="mt-text-label" class="a-form-label mt-label"></label>
								<span class="a-declarative">
								<input style="max-width: 30pt;" type="text" maxlength="8" value="[IN_STOCK]" class="a-input-text main-entry mt-input-text" data-initial="[IN_STOCK]">
								</span> </div>
							</div>
						  </div></td>
						<td class="mt-cell mt-right"><div class="mt-combination mt-layout-block">
							<div>
							  <div class="mt-link mt-wrap-bw"> <a class="a-link-normal mt-link-content mt-table-main" target="_blank" rel="noopener" href="http://www.amazon.com.au/gp/offer-listing/B0119IGNB6"> $[PRODUCT_PRICE]</a></div>
							</div>
							<div>
							  <div class="mt-text mt-wrap-bw"> <span class="mt-text-content mt-table-detail">[SHIPPING_COST]</span></div>
							</div>
						  </div></td>
					 	<td class="mt-cell mt-right"><div class="mt-combination mt-layout-block">
							  <div class="mt-text mt-wrap-bw"> <span class="mt-text-content mt-table-main" style="color: #b10000;">[EST_SALES_TAX]</span>
							</div>
							<div>
							  <div class="mt-text mt-wrap-bw"><span class="mt-text-content mt-table-detail"" style="color: #b10000;">[SALEX_TAX_PERC]</span></div>
							</div>
							</div></td>
						  <td class="mt-cell mt-right"><div class="mt-combination mt-layout-block">
							<div>
							  <div class="mt-link mt-wrap-bw"><a class="a-link-normal mt-table-main" target="_blank" rel="noopener">[PLATFORM]</a></div>
							</div>
							<div>
							  <div class="mt-text mt-wrap-bw"><span class="mt-text-content mt-table-detail">[SUPPLIER_NAME]</span></div>
							</div>
						  </div></td>
						 <td class="mt-cell mt-right"><div class="mt-combination mt-layout-block">
							<div>
							  <div class="mt-link mt-wrap-bw">[STARS]</div>
							</div>
							<div>
							  <div class="mt-text mt-wrap-bw"> <span class="mt-text-content mt-table-detail">[VOTES]</span></div>
							</div>
						  </div></td>
						 <td class="mt-cell mt-right"><div class="mt-combination mt-layout-block">
							<div>
							  <div class="mt-link mt-wrap-bw">[SALES_RANK]</div>
							</div</td>
						<td class="mt-cell mt-center"><div class="mt-text mt-wrap-bw"> <span class="mt-text-content">[UPC_EAN]</span></div></td>
						<td class="mt-cell mt-center" style="width: 10px;">
							<div class="mt-save-button-dropdown-normal"> <span class="a-splitdropdown-container">
                              <select name="" tabindex="-1" class="a-native-splitdropdown predisabled">
                              	<option selected="selected"> Edit </option>
                              	<option id="[SKU]" value="[SKU]" > List at shop </option>
                                <option> Request update </option>
                                <option> Delete product and listing </option>
                              </select>
                              <span tabindex="-1" data-a-class="main-entry mt-button mt-dropdown" class="a-button-group a-button-group-splitdropdown main-entry mt-button mt-dropdown">
	                              <span class="a-button a-button-group-first" id="a-autoid-1"><span class="a-button-inner">
	                              <button class="a-button-text a-text-left a-declarative" data-action="a-splitdropdown-main" type="button" id="a-autoid-1-announce"><span class="a-dropdown-prompt">Edit</span></button>
	                              </span></span>
	                              <span class="a-button a-button-group-last a-button-splitdropdown" id="a-autoid-2">
	                              <span class="a-button-inner">
	                              <button class="a-button-text a-declarative" data-action="a-splitdropdown-button" type="button" aria-hidden="true" id="a-autoid-2-announce" aria-pressed="false">
	                              <i class="a-icon a-icon-dropdown"></i></button>
	                              </span></span></span>
                              </span>
                            </div>
						</td>
					  </tr>'''

		# ------------- PREPARE ------------------------

		# Format time
		try:
			time_creation = datetime.utcfromtimestamp(int(product_temp['time_creation'])).strftime('%b %d, %Y %H:%M')	# %Y-%m-%d %H:%M
		except Exception as e:
			time_creation = 'N/A'
		# Time Update
		try:
			# time_update = datetime.utcfromtimestamp(int(product_temp['time_update'])).strftime('%Y-%m-%d %H:%M')
			# Assign time creation to update if not updated before
			if product_temp['time_update'] == None:
				product_temp['time_update'] = product_temp['time_creation']
			time_diff = time.time() - product_temp['time_update']
			if time_diff <= 60: time_update = str(int(time_diff)) + ' seconds ago'													# Seconds
			elif time_diff <= 60 * 60: time_update = str(int(time_diff / 60)) + ' minutes ago'										# Minutes
			elif time_diff <= 24 * 60 * 60: time_update = str(int(time_diff / 60 / 60)) + ' hours ago'								# Hours
			elif time_diff <= 7 * 24 * 60 * 60: time_update = str(int(time_diff / 60 / 60 / 24)) + ' days ago'						# Days
			elif time_diff <= 4 * 7 * 24 * 60 * 60: time_update = str(int(time_diff / 60 / 60 / 24 / 7)) + ' week ago'				# Week
			elif time_diff <= 52 * 4 * 7 * 24 * 60 * 60: time_update = str(int(time_diff / 60 / 60 / 24 / 7 / 4)) + ' month ago'	# Month
			else:
				year_temp = int(time_diff / 60 / 60 / 24 / 7 / 52)							# Year
				if year_temp == 0:
					year_temp = 1
					time_update = str(year_temp) + ' year ago'
		except Exception as e:
			time_update = 'Outdated'
		# Image
		try:
			product_temp['images_url'] = product_temp['images_url'][0]
		except Exception as e:
			product_temp['images_url'] = "{{ url_for('static', filename='img/default-product-small.png') }}"
		# Sale Status
		if product_temp['on_sale'] == True: tr_product = tr_product.replace('[STATUS]', 'Active')
		else: tr_product = tr_product.replace('[STATUS]', 'Disactive')
		# Merchant Name
		try:
			if len(product_temp['merchants'][0]['name']) >= 23: product_temp['merchants'][0]['name'] = str(product_temp['merchants'][0]['name'][:23]) + '<br>' + str(product_temp['merchants'][0]['name'][23:])
			if len(product_temp['merchants']) > 1: merchant_temp = product_temp['merchants'][0]['name'] + ' (+' + str(len(product_temp['merchants']) - 1) + ')'
			else: merchant_temp = product_temp['merchants'][0]['name']
		except Exception as e:
			merchant_temp = 'N/A'
		# Stars
		if product_temp['rating']['stars'] == None: product_temp['rating']['stars'] = 'N/A'						# Stars
		else: product_temp['rating']['stars'] = '&#11089; ' + str(product_temp['rating']['stars'])
		# Votes
		if product_temp['rating']['vote_total'] == None: product_temp['rating']['vote_total'] = 'N/A'			# Votes
		else: product_temp['rating']['vote_total'] = "{:,}".format(product_temp['rating']['vote_total'])
		# Sales Rank
		if product_temp['rating']['sales_rank'] != None: product_temp['rating']['sales_rank'] = "{:,}".format(product_temp['rating']['sales_rank'])
		else: product_temp['rating']['sales_rank'] = 'N/A'

		# ------------- SHIPPING -----------------------

		try:
			for ship in product_temp['shipping']:
				if ship['to_country'] == 'US':
					product_temp['shipping'][0]['shipping_cost'] = ship['shipping_cost']
					break
			tr_product = tr_product.replace('[SHIPPING_COST]', '+ $' + str(product_temp['shipping'][0]['shipping_cost']))
		except Exception as e:
			tr_product = tr_product.replace('[SHIPPING_COST]', 'N/A')

		# ------------- IDENTIFIERS --------------------

		if product_temp['identifier']['upc'] != None: tr_product = tr_product.replace('[UPC_EAN]', str(product_temp['identifier']['upc']))
		elif product_temp['identifier']['ean'] != None: tr_product = tr_product.replace('[UPC_EAN]', str(product_temp['identifier']['ean']))
		else: tr_product = tr_product.replace('[UPC_EAN]', 'N/A')


		# ------------- SALES TAX ----------------------

		est_sales_tax = '+ $' + '{0:,.2f}'.format(product_temp['variants'][0]['price_options'][0]['price'] * CONFIG['state-tax'])
		sales_tax_perc = f"{round(CONFIG['state-tax'], 3)}%"

		# ------------- EDIT HTML ----------------------

		tr_product = tr_product.replace('[PRODUCT_ID]', str(prod_id))
		tr_product = tr_product.replace('[SKU]', str(product_temp['identifier']['sku']))
		tr_product = tr_product.replace('[CONDITION]', 'New')	# INCOMPLETE
		tr_product = tr_product.replace('[PRODUCT_TITLE]', str(product_temp['title']))
		tr_product = tr_product.replace('[PLATFORM]', str(product_temp['platform_name']))
		tr_product = tr_product.replace('[IMAGE_URL]', str(product_temp['images_url']))
		tr_product = tr_product.replace('[ASIN]', str(product_temp['identifier']['asin']))
		tr_product = tr_product.replace('[TIME_CREATION]', time_creation)
		tr_product = tr_product.replace('[TIME_UPDATE]', time_update)
		tr_product = tr_product.replace('[IN_STOCK]', str(product_temp['variants'][0]['price_options'][0]['stock_count']))
		tr_product = tr_product.replace('[PRODUCT_PRICE]', str(product_temp['variants'][0]['price_options'][0]['price']))
		tr_product = tr_product.replace('[EST_SALES_TAX]', est_sales_tax)
		tr_product = tr_product.replace('[SALEX_TAX_PERC]', sales_tax_perc)
		tr_product = tr_product.replace('[SUPPLIER_NAME]', str(merchant_temp))
		tr_product = tr_product.replace('[STARS]', str(product_temp['rating']['stars']))
		tr_product = tr_product.replace('[VOTES]', str(product_temp['rating']['vote_total']))
		tr_product = tr_product.replace('[SALES_RANK]', str(product_temp['rating']['sales_rank']))

		# Add to <tr>
		tr_all = tr_all + '\n' + tr_product

		# ----------------------------------------------

	html_doc = html_doc.replace('''<tr><td>[PLACEHOLDER]</td></tr>''', tr_all)
	# Add timer
	time_load = str(round(time.time() - time_page_start, 2)) + ' secs'
	print(f"{logz.timestamp()}{Fore.YELLOW} WEB-APP → CATALOG → {Style.RESET_ALL}Page rendered in {time_load}")
	# Return
	return render_template_string(html_doc, **locals())

# [ ---------------------------------------------- ]


if __name__ == "__main__":
	# Connect to DB
	r = postgres.connect_db()
	if r == False:
		print(f"{logz.timestamp()}{Style.BRIGHT} WEB-APP → DB → Cannot connect")
	# Start Web App
	app.run(debug=True, host='0.0.0.0', port='4000', threaded=True)
