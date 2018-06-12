import os
import json
import random

path = '../../InputData'

pair_count = 0
keywords_count = 0

# find each urls.json file under data root
def find_target_file(path):
	global pair_count
	global keywords_count

	if os.path.isfile(path):
		if path.endswith('pairs.json'):
			pair_count += 1
			process_each_pair(path)
			dir_name = os.path.dirname(path)
			if os.path.exists(dir_name + '/keywords_pairs.json'):
				keywords_count += 1
				process_each_keywords_pair(dir_name + '/keywords_pairs.json')
	else:
		for subpath in os.listdir(path):
			find_target_file(path + '/' + subpath)


def process_each_pair(file):

	with open(file) as f:
		pairs = json.load(f)

	for pair in pairs:
		if pair['papers'] == [] or len(pair['papers']) == 0:
			continue

		first = pair['blog_title'].replace('\u2013', '').replace('\t', ' ').replace('\n', '')

		if first == '' or len(first) == 0:
			continue

		prev_paper_urls = set()  # prevent duplicated papers 

	
		for paper in pair['papers']:
			if paper['paper_url'] in prev_paper_urls:
				continue
			prev_paper_urls.add(paper['paper_url'])
			second = paper['paper_title'].replace('\u2013', '').replace('\t', ' ').replace('\n', '')
			# print(first + '\t' + second + '\t1')
			with open('titles_latest.train', 'a') as f:
				f.write(first + '\t' + second + '\t1\n')



def process_each_keywords_pair(file):

	dir_name = os.path.dirname(file)

	with open(file) as f:
		pairs = json.load(f)

	for pair in pairs:
		if pair['papers'] == [] or len(pair['papers']) == 0:
			continue

		first = pair['blog_keywords'].replace('\u2013', '').replace('\t', ' ').replace('\n', '')

		if first == '' or len(first) == 0:
			continue

		prev_paper_urls = set()  # prevent duplicated papers 

	
		for paper in pair['papers']:
			if paper['paper_url'] in prev_paper_urls:
				continue
			prev_paper_urls.add(paper['paper_url'])
			second = paper['paper_keywords'].replace('\u2013', '').replace('\t', ' ').replace('\n', '')
			# print(first + '\t' + second + '\t1')
			with open('keywords_new.train', 'a') as f:
				f.write(first + '\t' + second + '\t1\n')



def randomly_generate_negative_data(ratio):
	with open('titles_latest.train') as f:
		positive_data = f.readlines()
	size = len(positive_data)
	print(size)

	for each in positive_data:
		with open('titles_latest_'  + str(ratio + 1) + '.train', 'a') as f:
			f.write(each)

		lineX = each.split('\t')
	
		for i in range(0, ratio):
			while(True):
				random_id = random.randint(1, size - 1)
				print(random_id)
				lineY = positive_data[random_id].split('\t')
				if lineX[0] != lineY[0]:
					break
			with open('titles_latest_'  + str(ratio + 1) + '.train', 'a') as f:
				f.write(lineX[0] + '\t' + lineY[1] + '\t0\n')
			# try:
			# 	print(lineX[0] + '\t' + lineY[1] + '\t0\n')
			# except:
			# 	print(lineY)
			# 	print(random_id)
			# 	return
			



def main():
	# find_target_file(path)
	# print('pair_count: ' + str(pair_count))
	# print('keywords_count: ' + str(keywords_count))
	randomly_generate_negative_data(2) # ratio = negative/positive

main()