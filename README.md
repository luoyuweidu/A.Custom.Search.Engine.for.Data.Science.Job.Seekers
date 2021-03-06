# A Custom Job Search Engine for Data Science Job Seekers
Please click the link to access to the app
https://thawing-tundra-10605.herokuapp.com/

## Introduction
Now that I am looking for an analytics full-time job, I spend a lot of time searching and looking at online job posts on job boards like LinkedIn and Indeed. But I noticed that the job responsibilities of Data Analyst vary greatly from one post to another, and only a small portion of jobs I would consider good matches for my skills. Then I had the idea of creating a custom search engine that matches my resume with online job posts automatically so that I can apply from the top match if I  have limited time.

I'm new to the website scraping and app development, so I am learning as I go :)

Steps I'm taking to complete this project are:

1. Scrap and analyze 2000+ job post on Indeed to extract popular skills required by employers. This step generates a set of key words that are later used to perform hard skills match.
2. Write python codes that can takes one resume and parse them into key words.
3. Write a Python scaper that automatically scapes all the posts related to Data Scientist position on Indeed. Use the same text parsing process in step 2 to generate a set of key words for every post.
4. Calculate the degree of match between the set of key words from resume and key words from each post. A score is generated to represent the degree of match. The higher the better.
5. Display all the links ordered by the scores of match so that we can apply the most match at first!
6. Create html element and deploy the app on heroku.



## Instruction for user

1. First, the app would ask you to upload a resume.
![alt text](https://github.com/luoyuweidu/App/blob/master/Picture/Screen%20Shot%202017-03-31%20at%2022.08.10.png "Logo Title Text 1")

2. After uploading your resume, the website would ask you to enter the city and state you would like to look for a job in

![alt text](https://github.com/luoyuweidu/App/blob/master/Picture/Screen%20Shot%202017-03-31%20at%2022.08.28.png "Logo Title Text 1")

3. After you submit, the app would take a while(15-20 seconds) to fetch all the jobs back for you 
![alt text](https://github.com/luoyuweidu/App/blob/master/Picture/Screen%20Shot%202017-03-31%20at%2022.09.14.png "Logo Title Text 1")

## Explanation for files
