from argparse import ArgumentParser
from utils import *

 
tags = [
	'economy',
	'economics',
	'finance',
	'science',
	'technology',
	'blockchain',
	'biology',
	'mathematics',
	'physics',
	'chemistry',
	'medicine',
	'environment',
	'astronomy',
	'computer-science'
	'deep-learning', 
	'machine-learning', 
	'artificial-intelligence', 
	'ai', 
	'computer-vision', 
	'neural-networks',
	'data-science',
	'nlp',
	'naturallanguageprocessing'
]

def main():
	parser = ArgumentParser()
	parser.add_argument('-dr', '--DATA_ROOT', 
		default='../InputData', help='root directory to store data')
	parser.add_argument('-ur', '--URL_ROOT',
		default='https://medium.com/tag/', help='url root to crawl from')
	parser.add_argument('-sy', '--START_YEAR',
		default=2008, help='start year to crawl from')
	parser.add_argument('-ey', '--END_YEAR',
		default=2018, help='end year to crawl from')
	parser.add_argument('-sm', '--START_MONTH',
		default=1, help='start month to crawl from')
	parser.add_argument('-em', '--END_MONTH',
		default=12, help='end month to crawl from')
	parser.add_argument('-sd', '--START_DAY',
		default=1, help='start day to crawl from')
	parser.add_argument('-ed', '--END_DAY',
		default=31, help='end day to crawl from')
	parser.add_argument('-t', '--TAG',
		default=0, help='choose one medium tag to crawl from: (0 - ' + str(len(tags) - 1) + ')')

	args = parser.parse_args()

	global DATA_ROOT, URL_ROOT, START_YEAR, END_YEAR, START_MONTH, END_MONTH, START_DAY, END_DAY, TAG
	DATA_ROOT = args.DATA_ROOT	
	URL_ROOT = args.URL_ROOT
	START_YEAR = int(args.START_YEAR)
	END_YEAR = int(args.END_YEAR)
	START_MONTH = int(args.START_MONTH)
	END_MONTH = int(args.END_MONTH)
	START_DAY = int(args.START_DAY)
	END_DAY = int(args.END_DAY)
	TAG = tags[int(args.TAG)]
	print 'You are crawling ' + URL_ROOT + TAG + ' between date range: ' + \
	str(START_MONTH) + '/' + str(START_DAY) + '/' + str(START_YEAR) + '~' + \
	str(END_MONTH) + '/' + str(END_DAY) + '/' + str(END_YEAR) + \
	'. Crawled data will be saved to ' + DATA_ROOT

	crawl_each_tag(TAG) # crawl the requested tag

	# crawl the other tags (Optional)
	for other_tag in tags:
		if other_tag == TAG:
			continue
		crawl_each_tag(other_tag)

# crawl all the blogs under a given tag
def crawl_each_tag(tag):
	for year in range(START_YEAR, END_YEAR + 1):
		year_str = convert_number_to_str(year)
		path = URL_ROOT + tag + '/archive/' + year_str
		if check_redirect(path):
			continue
		# save to the first day of the year to prevent empty year(can be overridden)
		crawl_each_tag_by_day(year_str, '01', '01', tag)

		for month in range(START_MONTH, END_MONTH + 1):
			month_str = convert_number_to_str(month)
			path = URL_ROOT + tag + '/archive/' + year_str + '/' + month_str
			if check_redirect(path):
				continue
			# save to the first day of the month to prevent empty month(can be overridden)
			crawl_each_tag_by_day(year_str, month_str, '01', tag)

			for day in range(START_DAY, END_DAY + 1):
				day_str = convert_number_to_str(day) 
				# check if file already exist
				dir_name = DATA_ROOT + '/' + URL_ROOT.split('/')[2] + '/tags/' + tag + '/' + year_str + month_str + day_str
				if is_file_exist(dir_name + '/articles.json'):
					continue
				# check if the day exists
				path = URL_ROOT + tag + '/archive/' + year_str + '/' + month_str + '/' + day_str
				if check_redirect(path):
					continue
				crawl_each_tag_by_day(year_str, month_str, day_str, tag)
	
# crawl all the blogs under a given tag on a given day
def crawl_each_tag_by_day(year, month, day, tag):
	dir_name = DATA_ROOT + '/' + URL_ROOT.split('/')[2] + '/tags/' + tag + '/' + year + month + day
	if is_file_exist(dir_name + '/articles.json'):
		return
	path = URL_ROOT + tag + '/archive/' + year + '/' + month + '/' + day
	print 'crawl: ' + path

	# extract all urls from each day
	urls = extract_whole_page_urls(path, '//div[@class=\'postArticle-readMore\']/a')

	write_to_json_file(dir_name + '/urls.json', urls)
	
	#extract texts from each articles
	articles = extract_texts(urls)
	write_to_json_file(dir_name + '/articles.json', articles)


main()


