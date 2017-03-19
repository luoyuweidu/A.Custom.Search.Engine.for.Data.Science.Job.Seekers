# A Custom Job Search Engine for Data Science Job Seekers
Please click the link to access to the app
https://protected-bayou-42571.herokuapp.com

## Introduction
Now that I am looking for analytics full-time job, I spend a lot of time searching and looking at online job posts on job boards like LinkedIn and Indeed. But I noticed that the responsibilities of Data Analyst vary greatly one from another, and only a small portion of jobs I would consider good matches for my skills. I had the idea of creating a custom search engine that matches my resume with online job posts automatically so that I apply from the top match if I only have limited time.

I'm new to the website scraping and app development, so I am learning as I go :)

Steps I've taken to complete this project were:

1. Scraped and analyzed 2000+ job post on Indeed to extract popular skills required by employers. This step generated a set of key words that were lated used to perform hard skills match.
2. Wrote python codes that can takes one resume and parse them into key words.
3. Wrote a Python scaper that automatically scape all the posts related to Data Analyst position on Indeed. Use the same text parsing process to generate a set of key words for every posts.
4. Calculated the degree of match between the set of key words from resume and key words from each post. A score is generated to represent the degree of match. The higher the better.
5. Display all the links ordered by the scores of match so that we can apply the most match at first!
6. Create html element and deploy the app on heroku.



## Instruction for user

1. First, the app would ask you to upload a resume.
![alt text](https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Logo Title Text 1")

Reference-style: 


## Explanation for files
