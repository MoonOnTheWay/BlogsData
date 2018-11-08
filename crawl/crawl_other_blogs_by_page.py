from argparse import ArgumentParser
from utils import *
 

URL_LIST = [
	'https://research.fb.com/blog/page/',
	'https://machinelearningmastery.com/blog/page/',
	'https://www.analyticsvidhya.com/blog/page/',
	'https://dzone.com/artificial-intelligence-tutorials-tools-news/list?page=',
	'https://www.datacamp.com/community/tutorials?page=',
	'http://adventuresinmachinelearning.com/page/',
	'https://analyticsindiamag.com/category/learning-corner/page/',
	'https://deepmind.com/blog/?page=',
	'https://aws.amazon.com/cn/blogs/machine-learning/page/',
	'https://www.learnopencv.com/page/',
	'http://mccormickml.com/page',
	'http://blog.aylien.com/category/data-science/page/',
	'http://blog.aylien.com/category/research/page/',
	'http://blog.datumbox.com/page/',
	'https://datascience.stackexchange.com/questions?page=',
	'http://kvfrans.com/page/',
	'http://www.offconvex.org/page',
	'https://www.r-bloggers.com/page/',
]

URL_XPATH_MAP = {
	'https://research.fb.com/blog/page/': '//div[@class=\'panel-info\']/a',
	'https://machinelearningmastery.com/blog/page/': '//span[@class=\'read-more\']/a',
	'https://www.analyticsvidhya.com/blog/page/': '//h3[@class=\'entry-title short-bottom\']/a',
	'https://dzone.com/artificial-intelligence-tutorials-tools-news/list?page=': '//a[@class=\'article-toggle ng-binding\']',
	'https://www.datacamp.com/community/tutorials?page=': '//h2/a',
	'http://adventuresinmachinelearning.com/page/': '//h3[@class=\'entry-title mh-loop-title\']/a',
	'https://analyticsindiamag.com/category/learning-corner/page/': '//h5[@class=\'entry-title\']/a',
	'https://deepmind.com/blog/?page=': '//a[@class=\'faux-link-block--link\']',
	'https://aws.amazon.com/cn/blogs/machine-learning/page/': '//a[@class=\'blog-read-more blog-btn-a blog-btn-a-small\']',
	'https://www.learnopencv.com/page/': '//a[@class=\'more-link\']',
	'http://mccormickml.com/page': '//h1[@class=\'post-title\']/a',
	'http://blog.aylien.com/category/data-science/page/': '//div[@class=\'post--foot\']/a',
	'http://blog.aylien.com/category/research/page/': '//div[@class=\'post--foot\']/a',
	'http://blog.datumbox.com/page/': '//a[@class=\'btn-u btn-u-small\']',
	'https://datascience.stackexchange.com/questions?page=': '//h3/a',
	'http://kvfrans.com/page/': '//h2/a',
	'http://www.offconvex.org/page': '//a[@class=\'post-link\']',
	'https://www.r-bloggers.com/page/': '//a[@class=\'more-link\']',

}


def main():
	parser = ArgumentParser()
	parser.add_argument('-dr', '--DATA_ROOT', 
		default='../InputData', help='root directory to store data')
	parser.add_argument('-ur', '--URL_ROOT',
		default=0, help='url root to crawl from: (0 - ' + str(len(URL_LIST) - 1) + ')')
	parser.add_argument('-sp', '--START_PAGE',
		default=1, help='page to start from')
	parser.add_argument('-ep', '--END_PAGE',
		default=100, help='page to end to')

	args = parser.parse_args()

	global DATA_ROOT, URL_ROOT, START_PAGE, END_PAGE
	DATA_ROOT = args.DATA_ROOT	
	URL_ROOT = URL_LIST[int(args.URL_ROOT)] 
	START_PAGE = int(args.START_PAGE)
	END_PAGE = int(args.END_PAGE)
	print 'You are crawling ' + URL_ROOT + \
	' between page ' + str(START_PAGE) + ' and ' + str(END_PAGE) + \
	'. Crawled data will be saved to ' + DATA_ROOT

	crawl_each()

	chosen_url = URL_ROOT
	for other_url in URL_LIST:
		if other_url == chosen_url:
			continue
		URL_ROOT = other_url
		crawl_each()


# crawl each blog by page
def crawl_each():
	dir_name = DATA_ROOT + '/' + URL_ROOT.split('/')[2]
	if is_file_exist(dir_name + '/articles.json'):
		print 'exist: ' + dir_name
		return
	urls = []
	articles = []

	# handle the initial page path
	initial_path = URL_ROOT + str(START_PAGE)
	if check_404(initial_path):
		initial_path = URL_ROOT[:URL_ROOT.index('page')]
	if check_404(initial_path):
		return	
	print 'crawl: ' + initial_path
	urls.extend(extract_whole_page_urls(initial_path, URL_XPATH_MAP[URL_ROOT]))
	print len(urls)
	articles.extend(extract_texts(urls))

	for page in range(START_PAGE + 1, END_PAGE + 1):
		path = URL_ROOT + str(page)
		print 'crawl: ' + path
		if check_404(path):
			break	
		urls_each_page = extract_whole_page_urls(path, URL_XPATH_MAP[URL_ROOT])
		urls.extend(urls_each_page)
		print len(urls)
		articles_each_page = extract_texts(urls_each_page)
		articles.extend(articles_each_page)
	
	write_to_json_file(dir_name + '/urls.json', urls)
	write_to_json_file(dir_name + '/articles.json', articles)


main()
