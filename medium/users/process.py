import subprocess
import os
import time
import json

for dir_name in os.listdir('.'):
	if dir_name == '.DS_Store':
		continue
	input = dir_name + '/articles.json'
	output = dir_name + '/urls.json'
	urls = []
	try:
		with open(input, 'r') as f:
			articles = json.load(f)
	except:
		print dir_name
		continue

	for article in articles:
		urls.append(article['url'])

	with open(output, "w") as f:
	    f.write(json.dumps(urls, indent=4))

	# dir_name = filename[:len(filename) - 5]
	# subprocess.Popen('mkdir ' + dir_name, stdout=subprocess.PIPE, shell = True)
	# time.sleep(1)
	# subprocess.Popen('mv ' + filename + ' ' + 'articles.json', shell = True)
	# subprocess.Popen('mv articles.json ' + dir_name + '/', shell = True)
	