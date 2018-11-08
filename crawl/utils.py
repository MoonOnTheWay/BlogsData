import json
import os
import errno
import requests
import time
from goose import Goose
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

chrome_options = Options()  
chrome_options.add_argument("--headless")  

# crawl all the blog links given a page link
def extract_whole_page_urls(url, xpath):
	driver = webdriver.Chrome(chrome_options=chrome_options)
	wait = WebDriverWait(driver, 5)
	# driver.set_page_load_timeout(20)

	try:
		driver.get(url)
	except:
		print 'fail to get page link'
		driver.quit()
		return []

	SCROLL_PAUSE_TIME = 4
	# Get scroll height
	last_height = driver.execute_script("return document.body.scrollHeight")

	while True:
		# Scroll down to bottom
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		# Wait to load page
		time.sleep(SCROLL_PAUSE_TIME)
		# Calculate new scroll height and compare with last scroll height
		new_height = driver.execute_script("return document.body.scrollHeight")
		if new_height == last_height:
			break
		last_height = new_height

	divs = driver.find_elements_by_xpath(xpath)

	urls = []
	for div in divs:
		try:
			url = div.get_attribute('href')
		except:
			continue
		if url == None or len(url) == 0:
			continue
		print url
		urls.append(url)

	driver.quit()
	return urls


# extract the contents of a list of webpages using Goose
def extract_texts(urls):
	output = []
	for url in urls:
		output.append(extract_single_text(url))
		print len(output)
	return output

# extract the content of a single webpage using Goose
def extract_single_text(url):
	output = {}
	goose = Goose()
	try:
		article = goose.extract(url=url)
	except:
		return output
	title = article.title
	text = article.cleaned_text
	output['url'] = url
	output['title'] = title
	output['text'] = text	
	return output

# check if file exist
def is_file_exist(filename):
	if os.path.exists(filename):
		print 'exist: ' + filename
		return True
	else:
		print 'not exist: ' + filename
		return False

# write to json file
def write_to_json_file(filename, content):
	if not os.path.exists(os.path.dirname(filename)):
		try:
			os.makedirs(os.path.dirname(filename))
		except OSError as exc: # Guard against race condition
			if exc.errno != errno.EEXIST:
				raise
	with open(filename, "w") as f:
		f.write(json.dumps(content, indent=4))
		print 'write to: ' + filename

# convert interger year/month/day to string
def convert_number_to_str(number):
	if number < 10:
		string = '0' + str(number)
	else:
		string = str(number)
	return string

# check if there is redirect
def check_redirect(url):
	r = requests.get(url)
	if r.status_code == 404:
		return True
	if len(r.history) == 0 or len(r.history) == 2:
		return False
	else:
		print 'redirect: ' + url
		return True

# def check_redirect2(url):
# 	r = requests.get(url)

# check 404
def check_404(url):
	if requests.get(url).status_code == 404:
		print '404: ' + url
		return True
	else:
		return False