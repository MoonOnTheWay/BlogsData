import arxiv
import urllib.request
from urllib.request import urlretrieve
import json
from summa import summarizer
from summa import keywords
from rake_nltk import Rake
import os
from io import StringIO 
import time
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
 
path = '../../InputData'


# find each urls.json file under data root
def process_urls_file(path):
	# if path.startswith('../../InputData/www.r-bloggers.com'):
	# 	return
	if os.path.isfile(path):
		if path.endswith('articles.json'):
			process_each_pair(path)
	else:
		for subpath in os.listdir(path):
			process_urls_file(path + '/' + subpath)


def process_each_pair(file):
	dir_name = os.path.dirname(file)
	if os.path.exists(dir_name + '/keywords_pairs.json'):
		print('exists')
		return

	try:
		with open(dir_name + '/articles.json') as f:
			articles = json.load(f)
		with open(dir_name + '/linked_papers.json') as f:
			linked_papers = json.load(f)
	except:
		print('articles.json or linked_papers.json not exist under ' + dir_name)
		return

	if articles == [] or len(articles) == 0 or linked_papers == [] or len(linked_papers) == 0:
		return

	outputs = []

	for i in range(0,len(articles)):
		output = {}
		article = articles[i]

		try:
			output['blog_url'] = article['url']
			output['blog_title'] = article['title']
			# extract blog keywords from blog title and whole texts

			list = extract_keywords(article['title'] + '\n' + article['text'])

			output['blog_keywords'] = stemming_keywords(list)

			output['papers'] = []
			papers = linked_papers[i]['papers']
		except:
			continue

		for j in range(0, len(papers)):
			try:
				if not papers[j].startswith('https://arxiv.org/pdf/'):
					# print('not arxiv')
					continue
			except:
				print(file)
				continue

			try:
				arxiv_id = papers[j].split('/')[4]
				if arxiv_id.endswith('.pdf'):
					arxiv_id = arxiv_id[:-4]
				print(arxiv_id)
				pdf_title = arxiv.query(id_list=[arxiv_id])[0].title
				pdf_summary = arxiv.query(id_list=[arxiv_id])[0].summary
			except:
				continue

			each_paper = {}
			each_paper['paper_url'] = papers[j]
			each_paper['paper_title'] = pdf_title
			# extract paper keywords from paper title and summary
			
			existed_keywords = set()
			ps = PorterStemmer()

			list = extract_keywords(pdf_title + '\n' + pdf_summary)

			each_paper['paper_keywords'] = stemming_keywords(list)

			output['papers'].append(each_paper)
			# print(output)

		outputs.append(output)

	with open(dir_name + '/keywords_pairs.json', 'w') as f:
		print('write to ' + dir_name)
		f.write(json.dumps(outputs, indent=4))


def stemming_keywords(list):
	existed_keywords = set()
	keywords = []
	ps = PorterStemmer()

	for each in list:
		stemmed = ps.stem(each)
		if stemmed in existed_keywords:
			continue
		existed_keywords.add(stemmed)
		keywords.append(each)

	return ' '.join(keywords)



def extract_keywords(text):
	return keywords.keywords(text, split=True)
	# r = Rake()
	# r.extract_keywords_from_text(text)
	# return r.get_ranked_phrases()


def main():
	process_urls_file(path)

main()



