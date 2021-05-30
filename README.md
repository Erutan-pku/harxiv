# HArXiv

>  A highlight tool for reading ArXiv papers.



### How to Install

1. Clone this repo.

> git clone https://github.com/Erutan-pku/harxiv.git

2. Install Scrapy

> See https://doc.scrapy.org/en/latest/intro/install.html

### How to Run

1. Download the information of arxiv papers and save to arxiv_20210529.json.

> time scrapy crawl arxiv -o arxiv_20210529.json

2. Use arxiv_20210529.json to generate a web page with highlight.

> python3 postdeal.py arxiv_20210529.json arxiv_20210529.html 

### Configuration

See config.json. You can change the subject (spider:domain)，ignore some subject or some conference name in description (ignore_subj and ignore_desp), highlight some phrase in title, or highlight some author.

    {
    
      "spider": {
      
        "domain": "cs.CL", 
        
        "top_n" : 9999 
        
      },
       
      "ignore_subj": ["Sound (cs.SD)", "Audio and Speech Processing (eess.AS)"],
      
      "ignore_desp": ["INTERSPEECH"],
      
      "title_highlight": [
      
        ["lower_weight", ["Summarization", "Machine Translation"]],
        
        ["blue", ["Named Entity Recognition"]],
        
        ["red", ["Question Answering", "Question Generation", "Reading Comprehension"]]
        
      ],
      
      "author_highlight": [
      
        ["red", ["Zhiyuan Liu", "Maosong Sun"]]
        
      ]
      
    }
