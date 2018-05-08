## Data Structure

-Blogs
	-medium
		-tags
			-tag1
				-2018/05/01
					-urls.json
					-articles.json
				-...
			-...
		-users 
			-user1:
				-urls.json
				-articles.json
			-...

	-deeplearning4j

Note: 
urls.json only contains the article links
articles.json contains the links, titles, and texts of articles


## Architecture for crawling Medium

1. medium.com
	1. Under Tag: https://medium.com/tag/
		1. deep-learning
		2. machine-learning
		3. artificial-intelligence
		4. ai
		5. computer-vision
		6. neural-networks
		7. data-science
		8. nlp
		9. Naturallanguageprocessing

	Under each tag:
		1. Top stories: https://medium.com/tag/neural-networks
		2. Latest Stories: https://medium.com/tag/neural-networks/latest
		3. Top writers only under artificial-intelligence: https://medium.com/tag/artificial-intelligence/top-writers
		4. All history blogs: https://medium.com/tag/artificial-intelligence/archive/2017/01/01

	2. Under UserID: https://medium.com/
		The IDs can be extracted from
			Base: https://medium.com/tag/artificial-intelligence/top-writers
			Dynamically added from: latest stories’ authors(monitoring new authors)
