import subprocess
import time
from datetime import date
from argparse import ArgumentParser

# time of crawling each website of each day/page
TIME_CRAW_EACH_WEBSITE_EACH_DAY_OR_PAGE = 300
NUM_MEDIUM_TAGS = 18
NUM_MEDIUM_TEMPLATES = 9
NUM_OTHER_BLOGS_BY_DATE = 4
NUM_OTHER_BLOGS_BY_PAGE = 19

parser = ArgumentParser()

def crawl_by_day():
	args = parser.parse_args()

	start_year = str(args.START_YEAR)
	end_year = str(args.END_YEAR)
	start_month = str(args.START_MONTH)
	end_month = str(args.END_MONTH)
	start_day = str(args.START_DAY)
	end_day = str(args.END_DAY)

	days_duration = (date(int(end_year), int(end_month), int(end_day)) - 
		date(int(start_year), int(start_month), int(start_day))).days + 1

	p = subprocess.Popen('exec ' + 'python2 crawl_blogs_medium_template.py -sy ' + start_year + ' -sm ' + start_month + ' -sd ' + start_day + \
		' -ey ' + end_year + ' -em ' + end_month + ' -ed ' + end_day, shell=True)
	timeout = TIME_CRAW_EACH_WEBSITE_EACH_DAY_OR_PAGE * days_duration * NUM_MEDIUM_TEMPLATES
	time.sleep(timeout)
	print 'time out after ' + str(timeout) + ' seconds\n'
	p.kill()

	p = subprocess.Popen('python2 crawl_blogs_medium.py -sy ' + start_year + ' -sm ' + start_month + ' -sd ' + start_day + \
		' -ey ' + end_year + ' -em ' + end_month + ' -ed ' + end_day, shell=True)
	timeout = TIME_CRAW_EACH_WEBSITE_EACH_DAY_OR_PAGE * days_duration * NUM_MEDIUM_TAGS
	time.sleep(timeout)
	print 'time out after ' + str(timeout) + ' seconds\n'
	p.kill()

	p = subprocess.Popen('python2 crawl_other_blogs_by_date.py -sy ' + start_year + ' -sm ' + start_month + ' -sd ' + start_day + \
		' -ey ' + end_year + ' -em ' + end_month + ' -ed ' + end_day, shell=True)
	timeout = TIME_CRAW_EACH_WEBSITE_EACH_DAY_OR_PAGE * days_duration * NUM_OTHER_BLOGS_BY_DATE
	time.sleep(timeout)
	print 'time out after ' + str(timeout) + ' seconds\n'
	p.kill()


def crawl_by_page():
	args = parser.parse_args()

	start_page = str(args.START_PAGE)
	end_page = str(args.END_PAGE)

	num_pages = int(end_page) - int(start_page) + 1

	p = subprocess.Popen('python2 crawl_other_blogs_by_page.py -sp ' + start_page + ' -ep ' + end_page, shell=True)
	timeout = TIME_CRAW_EACH_WEBSITE_EACH_DAY_OR_PAGE * num_pages * NUM_OTHER_BLOGS_BY_PAGE
	time.sleep(timeout)
	print 'time out after ' + str(timeout) + ' seconds\n'
	p.kill()


def main():
	#default is crawl daily blogs
	today = str(date.today()).split('-')
	parser.add_argument('-sy', '--START_YEAR',
		default=today[0], help='start year to crawl from')
	parser.add_argument('-ey', '--END_YEAR',
		default=str(int(today[0])), help='end year to crawl from')
	parser.add_argument('-sm', '--START_MONTH',
		default=today[1], help='start month to crawl from')
	parser.add_argument('-em', '--END_MONTH',
		default=str(int(today[1])), help='end month to crawl from')
	parser.add_argument('-sd', '--START_DAY',
		default=today[2], help='start day to crawl from')
	parser.add_argument('-ed', '--END_DAY',
		default=str(int(today[2])), help='end day to crawl from')

	# default is crawl the first(latest) page
	parser.add_argument('-sp', '--START_PAGE',
		default=1, help='page to start from')
	parser.add_argument('-ep', '--END_PAGE',
		default=2, help='page to end to')

	crawl_by_day()
	crawl_by_page()
	
main()

# time.sleep(50)
# p.kill()