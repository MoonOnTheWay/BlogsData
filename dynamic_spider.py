from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
from goose import Goose
import json
import os
import errno
import requests

DATA_ROOT = '../../BlogsData'

chrome_options = Options()  
chrome_options.add_argument("--headless")  

tags = [
	'deep-learning', 
	'machine-learning', 
	'artificial-intelligence', 
	'ai', 
	'computer-vision', 
	'neural-networks',
	'data-science',
	'nlp',
	'Naturallanguageprocessing'
	]

# crawl all the blog links given a page link by clicking on next button
def crawl_whole_page_urls_by_click(url):
	driver = webdriver.Chrome(chrome_options=chrome_options)
	wait = WebDriverWait(driver, 5)
	driver.set_page_load_timeout(300)
	driver.get(url)
	SCROLL_PAUSE_TIME = 1
	last_height = driver.execute_script("return document.body.scrollHeight")
	urls = []

	while True:
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		try:
			driver.find_element_by_xpath("//a[@class='posts older btn small']").click()
		except:
			break
		time.sleep(SCROLL_PAUSE_TIME)
		new_height = driver.execute_script("return document.body.scrollHeight")
		# if new_height == last_height:
		# 	break
		last_height = new_height
		divs = driver.find_elements_by_xpath("//ol[@id='posts-list']/li")
		for div in divs:
			try:
				url = div.find_element_by_css_selector('a').get_attribute('href')
			except:
				continue
			print url
			urls.append(url)

	# divs = driver.find_elements_by_xpath("//li")
	# urls = []
	# for div in divs:
	# 	try:
	# 		url = div.find_element_by_css_selector('a').get_attribute('href')
	# 	except:
	# 		continue
	# 	print url
	# 	urls.append(url)

	driver.quit()
	return urls

# crawl all the blog links given a page link
def crawl_whole_page_urls(url):
	driver = webdriver.Chrome(chrome_options=chrome_options)
	wait = WebDriverWait(driver, 5)
	# driver.set_page_load_timeout(20)

	try:
		driver.get(url)
	except:
		print 'continue'
		pass

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

	# divs = driver.find_elements_by_class_name('more-link')
	# divs = driver.find_elements_by_xpath("//a[@class='post-link']")
	# divs = driver.find_elements_by_xpath("//a[@class='more-link']")
	# divs = driver.find_elements_by_xpath("//h2[@class='entry-title']/a")
	# divs = driver.find_elements_by_xpath("//a[@class='faux-link-block--link']")
	# divs = driver.find_elements_by_xpath("//div[@class='summary']/h3/a")
	divs = driver.find_elements_by_xpath("//div[@class='postArticle-readMore']/a")


	urls = []
	for div in divs:
		try:
			url = div.get_attribute('href')
		except:
			continue
		# url = div.find_element_by_css_selector('a').get_attribute('href')
		if url == None or len(url) == 0:
			continue
		# if '/p/' not in url:
		# 	continue
		print url
		urls.append(url)

	print urls
	driver.quit()
	return urls

# extract the contents of a list of webpages using Goose
def extract_texts(urls):
	output = []
	for url in urls:
		output.append(extract_single_text(url))
		print len(output)
	return output

# extract the content of a single webpage using newspaper
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
	return os.path.exists(os.path.dirname(filename))	

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
		return True

# check 404
def check_404(url):
	return requests.get(url).status_code == 404

# crawl all the blogs under a given tag on a given day
def crawl_each_tag_by_day(root, year, month, day, tag):
	dir_name = year + month + day
	path = root + tag + '/archive/' + year + '/' + month + '/' + day
	print path
	# path = 'https://medium.com/tag/' + tag + '/archive/' + year + '/' + month + '/' + day

	# extract all urls from each day
	urls = crawl_whole_page_urls(path)

	write_to_json_file(DATA_ROOT + '/' + root.split('/')[2] + '/tags/' + tag + '/' + dir_name + '/urls.json', urls)
	# write_to_json_file(DATA_ROOT + '/tags/' + tag + '/' + dir_name + '/urls.json', urls)
	
	#extract texts from each articles
	articles = extract_texts(urls)
	write_to_json_file(DATA_ROOT + '/' + root.split('/')[2] + '/tags/' + tag + '/' + dir_name + '/articles.json', articles)
	# write_to_json_file(DATA_ROOT + '/tags/' + tag + '/' + dir_name + '/articles.json', articles)

# crawl all the blogs under a given tag
def crawl_each_tag(root, tag):
	for year in range(2014, 2016):
		year_str = convert_number_to_str(year)
		# check if the year exists
		# path = root + year_str
		# print path
		path = root + tag + '/archive/' + year_str
		if check_redirect(path):
			print 'redirect'
			continue

		for month in range(1, 13):
			month_str = convert_number_to_str(month)
			# check if the month exists
			# path = root + year_str + '/' + month_str
			path = root + tag + '/archive/' + year_str + '/' + month_str
			if check_redirect(path):
				print 'redirect'
				continue

			# save to the first day of the month to prevent empty month(can be overridden)
			crawl_each_tag_by_day(root, year_str, month_str, '01', tag)

			for day in range(1, 32):
				day_str = convert_number_to_str(day)

				# check if file already exist
				dir_name = year_str + month_str + day_str
				if is_file_exist(DATA_ROOT + '/' + root.split('/')[2] + '/tags/' + tag + '/' + dir_name + '/urls.json'):
				# if is_file_exist(DATA_ROOT + '/' + root.split('/')[2] + '/' + dir_name + '/urls.json'):
					print 'exist'
					continue

				# check if the day exists
				path = root + year_str + '/' + month_str + '/' + day_str

				# path = 'https://medium.com/tag/' + tag + '/archive/' + year_str + '/' + month_str + '/' + day_str
				if check_redirect(path):
					print 'redirect'
					continue
				crawl_each_tag_by_day(root, year_str, month_str, day_str, tag)

# crawl all the blogs under a given userID
def crawl_each_user(root):
	dir_path = '/' + root.split('/')[3]
	if is_file_exist(DATA_ROOT + dir_path + '/articles.json'):
		print 'exist'
		return

	urls = crawl_whole_page_urls(root)
	print len(urls)
	write_to_json_file(DATA_ROOT + dir_path + '/urls.json', urls)

	#extract texts from each articles
	articles = []
	for url in urls:
		articles.append(extract_single_text(url))
		print len(articles)
	write_to_json_file(DATA_ROOT + dir_path + '/articles.json', articles)
	


# crawl other blogs by page
def crawl_otherblogs(root):
	urls = []
	articles = []
	urls.extend(crawl_whole_page_urls(root))
	print len(urls)

	for tag in ['page']:
		for i in range(2, 46):
			path = root + tag + '/' + str(i)
			if check_404(path):
				break	
			# extract all urls from each day
			urls.extend(crawl_whole_page_urls(path))
			print len(urls)
	
	dirc = root.split('/')[2]
	write_to_json_file(DATA_ROOT + '/' + dirc + '/urls.json', urls)

	articles = extract_texts(urls)

	write_to_json_file(DATA_ROOT + '/' + dirc + '/articles.json', articles)

	
def main():
	root = 'https://medium.com/tag/'
	for tag in tags:
		crawl_each_tag(root, tag)


	# root = 'https://deepmind.com/blog/?page='

	# dir_path = '/' + root.split('/')[2] + '/'
	# urls = []
	# articles = []

	# for page in range(1, 9):
	# 	path = root + str(page)
	# 	urls.extend(crawl_whole_page_urls(path))	

	# write_to_json_file(DATA_ROOT + dir_path + '/urls.json', urls)

	# articles = extract_texts(urls)
	# write_to_json_file(DATA_ROOT + dir_path + '/articles.json', articles)



	# crawl_each_tag('')
	# root = 'https://medium.com/tag/artificial-intelligence/top-writers'
	# dirc = root.split('/')[2]
	# with open(DATA_ROOT + '/' + dirc + '/top_writers.json') as f:
	# 	writers = json.load(f)
	
	# for writer in writers:
	# 	id = writer.split('/')[3]
	# 	crawl_each_user(id)

main()

