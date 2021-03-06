## Detailed Description
Latest:
https://docs.google.com/document/d/14Deb-k031A-wUiR3ifdMr3lVuz9sOsmHXI7wC5UDito/edit?usp=sharing

Old:
https://docs.google.com/document/d/1K5yPhdy8FkSTsKnwMEHkopyy2D8NtYaD3-m8h7nZBdw/edit?usp=sharing

## Project Report
https://docs.google.com/document/d/1UVpz1pxvqckHqzREAUcwi6p17unVyfbEJTHBBN18Rk8/edit?usp=sharing

## Data Format
* blog_paper_pairs.json
  - 'blog_url': url of the article
  - 'blog_text': full texts of the article (extracted using Goose)
  - 'blog_keywords': list of keywords extracted from full texts (using rake-nltk)
  - 'papers': list of paper related to the article
    - 'paper_url': url of each paper
    - 'paper_text': title + abstract of each paper (downloaded using urlretrieve, extracted using pdfminer)
    - 'paper_keywords': list of keywords extracted from abstract of the paper (using rake-nltk)
  
* linked_papers.json
  - 'url': url of the article
  - 'papers': list of paper urls extracted from the article

* articles.json
  - 'url': url of the article
  - 'title': title of the article
  - 'text': content text of the article
  - 'website': (not required) website domain name
  - 'tag': (not required) could be tag, author name, or empty based on different websites
  - 'date': (not required) date of the article, could be empty
  
  
## Crawled Websites
- https://medium.com/tag/deep-learning/archive/2015/01/01, by tag
- https://medium.com/@shagun/latest, by user
- https://deeplearning4j.org/documentation
- https://theneuralperspective.com/tag/tutorials/, https://theneuralperspective.com/tag/readings/
- https://research.fb.com/blog/page/2/ 
- https://machinelearningmastery.com/blog/page/2/
- https://towardsdatascience.com/archive/2015/01/01 
- https://www.analyticsvidhya.com/blog/page/1/
- https://www.kdnuggets.com/tag/deep-learning/page/6
- http://deeplearning.net/tutorial/contents.html
- https://blog.acolyer.org/2017/05/05/
- http://neuralnetworksanddeeplearning.com/
- https://www.kaggle.com/kernels
- https://devblogs.nvidia.com/tag/deep-learning/#
- https://hackernoon.com/archive/2018/05/01
- https://www.tensorflow.org/tutorials/
- http://cs231n.github.io/
- http://neuralnetworksanddeeplearning.com/chap1.html
- https://medium.freecodecamp.org/tagged/machine-learning/
- https://becominghuman.ai/archive/2017/01
- https://www.jeremyjordan.me/data-science/
- https://leonardoaraujosantos.gitbooks.io/artificial-inteligence/content/
- https://www.microsoft.com/developerblog/tag/deep-learning
- http://ruder.io/index.html#open
- http://ufldl.stanford.edu/tutorial/
- http://www.wildml.com/2016/08/
- https://codeburst.io/tagged/artificial-intelligence
- https://www.datacamp.com/community/tutorials?page=9
- https://dzone.com/artificial-intelligence-tutorials-tools-news/list?page=23
- https://www.oreilly.com/ideas/topics/ai/page/4, https://www.oreilly.com/learning/topics/ai
- https://wiki.tum.de/display/lfdv/Advanced+Level, https://wiki.tum.de/display/lfdv/Basic+Level
- http://adventuresinmachinelearning.com/
- https://analyticsindiamag.com/category/learning-corner/page/3/
- https://ayearofai.com/latest
- https://deepmind.com/blog/?page=2
- https://machinelearnings.co/latest
- https://aws.amazon.com/cn/blogs/machine-learning/page/20/
- https://www.learnopencv.com/page/18/
- http://mccormickml.com/page12/
- http://ml-cheatsheet.readthedocs.io/en/latest/
- https://medium.com/neuromation-io-blog/latest
- http://blog.aylien.com/category/data-science/page/3/, http://blog.aylien.com/category/research/page/3/
- http://blog.datumbox.com/page/2/
- https://blog.slavv.com/latest
- http://colah.github.io/
- https://danijar.com/blog/
- https://datascience.stackexchange.com/questions?page=30&sort=frequent
- http://ischlag.github.io/
- https://medium.com/@karpathy/latest
- http://kvfrans.com/page/2/
- http://machinelearninguru.com/blog.php
- https://mattmazur.com/2018/05/18/
- http://www.offconvex.org/page2/
- https://www.pyimagesearch.com/page/26/
- https://www.r-bloggers.com/page/2/

  
  
## How to import to database
* All data are named "articles.json" under the root directory: /disk/home/muxu/BlogsData
* Run upload_to_poqaa.py


## Data Structure

- Blogs
  - medium
    - tags
      - tag1
        - 2018/05/01
          - urls.json
          - articles.json
        - ...
      - ...
    - users 
      - user1:
        - urls.json
        - articles.json
      - ...
  - deeplearning4j
    - articles.json


`Note:`  

urls.json only contains the article links

articles.json contains the links, titles, and texts of articles


## Architecture for crawling Medium

1. medium.com
   - Under Tag: https://medium.com/tag/artificial-intelligence
       - Under each tag:
         - Top stories: https://medium.com/tag/neural-networks
         - Latest Stories: https://medium.com/tag/neural-networks/latest
         - All history blogs: https://medium.com/tag/artificial-intelligence/archive/2017/01/01
         - Top writers: https://medium.com/tag/artificial-intelligence/top-writers

   - Under UserID: https://medium.com/@IntuitMachine/latest
     - The IDs can be extracted from
       - Base: https://medium.com/tag/artificial-intelligence/top-writers
       - Dynamically added from: latest stories’ authors(monitoring new authors)
