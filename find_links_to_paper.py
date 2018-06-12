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


chrome_options = Options()  
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-extensions')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')

DATA_ROOT = '../../InputData'

paper_links = [
	'aclweb.org',
	'researchgate.net',
	'semanticscholar.org',
	'nips.cc',
	'arxiv.org',
	'scholar.google.com',
	'openreview.net',
	'research.google.com',
	'dl.acm.org',
	'shortscience.org',
	'citeulike.org',
	'bibsonomy.org',
	'bibbase.org',
	'jmlr.org',
	'aaai.org',
	'ieeexplore.ieee.org',
	'sciencedirect.com'
]

block_links = [
	'colab.research.google.com'
]


# find each urls.json file under data root
def process_urls_file(path):
	if path.startswith('../../InputData/medium.com'):
		return

	if os.path.isfile(path):
		parse_blog(path)
	else:
		for subpath in os.listdir(path):
			process_urls_file(path + '/' + subpath)

# parse each blog url and crawl all the paper links in the webpage content
def parse_blog(path):
	if os.path.exists(os.path.dirname(path) + '/linked_papers.json'):
		print 'exists'
		return
	if not path.endswith('urls.json'):
		return
	with open(path) as f:
		urls = json.load(f)

	output = []
	dir_path = path[:len(path) - 10] + '/linked_papers.json'

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

		pdf = get_pdf(link)
		time.sleep(3)

		if not pdf == 'NULL':
			pdfs.append(pdf)

	content = {}
	content['url'] = url
	content['papers'] = pdfs

	print content
	return content



# check if the url is linked to a paper
def is_paper_link(url):
	if url == None:
		return False
	if url.endswith('pdf'):
		return True
	for each in block_links:
		if each in url:
			return False
	for each in paper_links:
		if each in url:
			return True

	# collect the filtered paper links
	# with open('filtered_paper_links.txt', 'a') as f:
		# f.write(url + '\n')
	return False


# get the .pdf link give a paper url
def get_pdf(url):
	if url.endswith('.pdf'):
		return url

	# time.sleep(1)
	driver = webdriver.Chrome(chrome_options=chrome_options)
	# wait = WebDriverWait(driver, 3)
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

	pdf = url
	for link in links:
		try:
			link = link['href']
		except:
			continue
		if link.startswith('/'):
			baseurl = url.split('/')[0] + '//' + url.split('/')[2] 
			link = baseurl + link
		if 'pdf' in link:
			pdf = link
			break

	return pdf


# write to json file
def write_to_json_file(filename, content):
	if not os.path.exists(os.path.dirname(filename)):
		try:
			os.makedirs(os.path.dirname(filename))
		except OSError as exc: # Guard against race condition
			if exc.errno != errno.EEXIST:
				raise
	print 'write to ' + filename + '\n'
	with open(filename, "w") as f:
		f.write(json.dumps(content, indent=4))

def main():
	process_urls_file(DATA_ROOT)

main()
