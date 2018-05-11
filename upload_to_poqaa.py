import requests
import json
import os


DATA_ROOT = '/disk/home/muxu/BlogsData'

url = 'http://poqaa.com/api/crawledWebpage/'

HEADERS = {
  "X-CSRFToken" : "Tti9uBoqYBTqPGWN0ejyFAqBfCW3Ed2xt8aR7mkATWJmhp8xIrhiivejMPs8sy4U",
  "Cookie": "csrftoken=Tti9uBoqYBTqPGWN0ejyFAqBfCW3Ed2xt8aR7mkATWJmhp8xIrhiivejMPs8sy4U"
}


def post_each_article(path):
	if not path.endswith('articles.json'):
		return
	try:
		with open(path) as f:
			articles = json.load(f)
	except:
		return

	for article in articles:
		response = requests.post(url, data=json.dumps(article), headers=HEADERS)
		print(response.content)

def find_file(path):
	if os.path.isfile(path):
		post_each_article(path)
	else:
		for subpath in os.listdir(path):
			find_file(path + '/' + subpath)
	
def main():
	find_file(DATA_ROOT)

main()

