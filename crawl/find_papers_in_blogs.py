import time
from goose import Goose
import json
import os
import errno
import requests
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from utils import write_to_json_file, is_file_exist
from argparse import ArgumentParser


chrome_options = Options()  
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-extensions')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')

def main():
	parser = ArgumentParser()
	parser.add_argument('-dr', '--DATA_ROOT', 
		default='../InputData', help='root directory to find linked papers')
	args = parser.parse_args()
	global DATA_ROOT
	DATA_ROOT = args.DATA_ROOT	
	process_urls_file(DATA_ROOT)


# find each down-most directory under data root
def process_urls_file(root):
	for dirpath, dirnames, filenames in os.walk(root):
		if not dirnames:
			parse_blog(dirpath)

# parse each blog url and crawl all the paper links in the webpage content
def parse_blog(path):
	if is_file_exist(path + '/linked_papers.json'):
		return
	if not is_file_exist(path + '/urls.json'):
		return

	with open(path + '/urls.json') as f:
		urls = json.load(f)

	output = []
	dir_path = path + '/linked_papers.json'

	for url in urls:
		output.append(crawl_paper_links(url))
		write_to_json_file(dir_path, output)


# crawl all the blog links given a page url
def crawl_paper_links(url): 
	driver = webdriver.Chrome(chrome_options=chrome_options)
	wait = WebDriverWait(driver, 3)
	# driver.set_page_load_timeout(180)

	try:
		driver.get(url)
	except:
		print 'continue'
		driver.quit()
		content = {}
		content['url'] = url
		content['papers'] = []
		return content

	soup = BeautifulSoup(driver.page_source, 'html.parser')
	driver.quit()

	links = soup.find_all('a')

	pdfs = []
	for link in links:
		try:
			link = link['href']
		except:
			continue
		if link.startswith('/'):
			baseurl = url.split('/')[0] + url.split('/')[1] + url.split('/')[2] 
			link = baseurl + link

		# check if is paper link
		if is_paper_link(link) == False:
			continue

		pdf = link
		# pdf = get_pdf(link)
		# time.sleep(3)

		if not pdf == 'NULL':
			pdfs.append(pdf)

	content = {}
	content['url'] = url
	content['papers'] = pdfs

	# print content
	return content


# check if the url is linked to a paper
def is_paper_link(url):
	if url == None:
		return False
	if url.endswith('pdf') or 'arxiv.org' in url:
		return True
	# collect the filtered paper links
	# with open('filtered_paper_links.txt', 'a') as f:
	# 	f.write(url + '\n')
	return False
	

main()
