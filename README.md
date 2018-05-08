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
