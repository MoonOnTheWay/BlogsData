from argparse import ArgumentParser
from utils import *

URL_LIST = [
	'https://www.r-bloggers.com/',
	'https://blog.acolyer.org/',
	'http://www.wildml.com/',
	'https://mattmazur.com/',
	'https://www.kdnuggets.com/',
]

URL_XPATH_MAP = {
	'https://www.r-bloggers.com/': '//a[@class=\'more-link\']',
	'https://blog.acolyer.org/': '//li/a',
	'http://www.wildml.com/': '//a[@class=\'more-link\']',
	'https://mattmazur.com/': '//h1[@class=\'entry-title\']/a',
	'https://www.kdnuggets.com/': '//li/a',
}


def main():
	parser = ArgumentParser()
	parser.add_argument('-dr', '--DATA_ROOT', 
		default='../InputData', help='root directory to store data')
	parser.add_argument('-ur', '--URL_ROOT',
		default=0, help='url root to crawl from: (0 - ' + str(len(URL_LIST) - 1) + ')')
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

	args = parser.parse_args()

	global DATA_ROOT, URL_ROOT, START_YEAR, END_YEAR, START_MONTH, END_MONTH, START_DAY, END_DAY
	DATA_ROOT = args.DATA_ROOT	
	URL_ROOT = URL_LIST[int(args.URL_ROOT)] 
	START_YEAR = int(args.START_YEAR)
	END_YEAR = int(args.END_YEAR)
	START_MONTH = int(args.START_MONTH)
	END_MONTH = int(args.END_MONTH)
	START_DAY = int(args.START_DAY)
	END_DAY = int(args.END_DAY)
	print 'You are crawling ' + URL_ROOT + ' between date range: ' + \
	str(START_MONTH) + '/' + str(START_DAY) + '/' + str(START_YEAR) + '~' + \
	str(END_MONTH) + '/' + str(END_DAY) + '/' + str(END_YEAR) + \
	'. Crawled data will be saved to ' + DATA_ROOT

	crawl_each()

	chosen_url = URL_ROOT
	for other_url in URL_LIST:
		if other_url == chosen_url:
			continue
		URL_ROOT = other_url
		crawl_each()

# crawl all the blogs
def crawl_each():
	for year in range(START_YEAR, END_YEAR + 1):
		year_str = convert_number_to_str(year)
		path = URL_ROOT + year_str + '/'
		if check_redirect(path) and check_redirect(path.strip('/')):
			continue
		# save to the first day of the year to prevent empty year(can be overridden)
		crawl_by_day(year_str, '', '')

		for month in range(START_MONTH, END_MONTH + 1):
			month_str = convert_number_to_str(month)
			path = URL_ROOT + year_str + '/' + month_str + '/'
			if check_redirect(path) and check_redirect(path.strip('/')):
				continue
			# save to the first day of the month to prevent empty month(can be overridden)
			crawl_by_day(year_str, month_str, '')

			for day in range(START_DAY, END_DAY + 1):
				day_str = convert_number_to_str(day) 
				# check if file already exist
				dir_name = DATA_ROOT + '/' + URL_ROOT.split('/')[2] + '/' + year_str + month_str + day_str
				if is_file_exist(dir_name + '/articles.json'):
					print 'exist: ' + dir_name
					continue
				# check if the day exists
				path = URL_ROOT + year_str + '/' + month_str + '/' + day_str + '/'
				if check_redirect(path) and check_redirect(path.strip('/')):
					continue
				crawl_by_day(year_str, month_str, day_str)
	
# crawl all the blogs on a given day
def crawl_by_day(year, month, day):
	if URL_ROOT.split('/')[2] == 'medium.com':
		dir_name = DATA_ROOT + '/' + URL_ROOT.split('/')[3] + '/' + year + month + day
	else:
		dir_name = DATA_ROOT + '/' + URL_ROOT.split('/')[2] + '/' + year + month + day

	if is_file_exist(dir_name + '/articles.json'):
		print 'exist: ' + dir_name
		return
	path = URL_ROOT + year + '/' + month + '/' + day + '/'
	print 'crawl: ' + path
	# extract all urls from each day
	urls = extract_whole_page_urls(path, URL_XPATH_MAP[URL_ROOT])

	write_to_json_file(dir_name + '/urls.json', urls)
	
	#extract texts from each articles
	articles = extract_texts(urls)
	write_to_json_file(dir_name + '/articles.json', articles)


main()
