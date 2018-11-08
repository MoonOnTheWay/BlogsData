import os
import json
from utils import is_file_exist
from argparse import ArgumentParser


def main():
	parser = ArgumentParser()
	parser.add_argument('-dr', '--DATA_ROOT', 
		default='../InputData', help='root directory to seek files')
	parser.add_argument('-fn', '--FILE_NAME', 
		default='urls.json', help='file name you are seeking')
	parser.add_argument('-kw', '--KEY_WORD',
		default='', help='key word in the file you are seeking')

	args = parser.parse_args()

	global DATA_ROOT, FILE_NAME, KEY_WORD, TOTAL_COUNT, UNIQUE_COUNT, MAP 
	TOTAL_COUNT = 0
	UNIQUE_COUNT = 0
	MAP = {}

	DATA_ROOT = args.DATA_ROOT	
	FILE_NAME = args.FILE_NAME
	KEY_WORD = args.KEY_WORD

	print 'You are counting ' + FILE_NAME + ' from ' + DATA_ROOT

	find_all_files()

	print 'Total Number: ' + str(TOTAL_COUNT)
	print 'Unique Number: ' + str(UNIQUE_COUNT)

# find each down-most directory under data root
def find_all_files():
	for dirpath, dirnames, filenames in os.walk(DATA_ROOT):
		if not dirnames:
			if FILE_NAME.startswith('urls'):
				count_urls(dirpath + '/' + FILE_NAME)
			elif FILE_NAME.startswith('linked_papers'):
				if 'arxiv' in KEY_WORD:
					count_linked_arxiv_papers(dirpath + '/' + FILE_NAME)
				else:
					count_linked_papers(dirpath + '/' + FILE_NAME)

def count_urls(file):
	if is_file_exist(file):
		with open(file) as f:
			urls = json.load(f)
			global TOTAL_COUNT, UNIQUE_COUNT, MAP
			TOTAL_COUNT += len(urls)
			for url in urls:
				MAP[url] = 1 #hashset, 1 is meaningless
				UNIQUE_COUNT += 1
			# print file + ' has ' + str(len(urls)) + ' urls.\n'

def count_linked_papers(file):
	if is_file_exist(file):
		with open(file) as f:
			try:
				data = json.load(f)
				global TOTAL_COUNT, UNIQUE_COUNT, MAP
				for each in data:
						TOTAL_COUNT += len(each['papers'])
						if not each['url'] in MAP:
							MAP[each['url']] = len(each['papers'])
							UNIQUE_COUNT += len(each['papers'])

			except:
				print 'except'

def count_linked_arxiv_papers(file):
	if is_file_exist(file):
		with open(file) as f:
			try:
				data = json.load(f)
				global TOTAL_COUNT, UNIQUE_COUNT, MAP
				for each in data:
						arxiv_count = 0
						for paper in each['papers']:
							if 'arxiv' in paper:
								arxiv_count += 1
						TOTAL_COUNT += arxiv_count
						if not each['url'] in MAP:
							MAP[each['url']] = arxiv_count
							UNIQUE_COUNT += arxiv_count
			except:
				print 'except'

main()








