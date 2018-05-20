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
- https://blog.acolyer.org/
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

## Data Format
* articles.json
  - 'url': url of the article
  - 'title': title of the article
  - 'text': content text of the article
  - 'website': website domain name
  - 'tag': (not required) could be tag, author name, or empty based on different websites
  - 'date': (not required) date of the article, could be empty
  
  
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
   - Under Tag: https://medium.com/tag/
     - deep-learning
     - machine-learning
     - artificial-intelligence
     - ai
     - computer-vision
     - neural-networks
     - data-science
     - nlp
     - naturallanguageprocessing
       - Under each tag:
         - Top stories: https://medium.com/tag/neural-networks
         - Latest Stories: https://medium.com/tag/neural-networks/latest
         - Top writers only under artificial-intelligence: https://medium.com/tag/artificial-intelligence/top-writers
         - All history blogs: https://medium.com/tag/artificial-intelligence/archive/2017/01/01
     
   - Under UserID: https://medium.com/
     - The IDs can be extracted from
       - Base: https://medium.com/tag/artificial-intelligence/top-writers
       - Dynamically added from: latest stories’ authors(monitoring new authors)
