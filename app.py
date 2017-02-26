from flask import Flask,render_template,request,redirect, url_for, send_from_directory
from werkzeug import secure_filename
import os

app_lulu = Flask(__name__, static_folder = 'static',static_url_path = '/static')

# This is the path to the upload directory a sql server?
app_lulu.config['UPLOAD_FOLDER'] = 'uploads/'

# These are the extension that we are accepting to be uploaded
app_lulu.config['ALLOWED_EXTENSIONS'] = set(['docx'])

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in app_lulu.config['ALLOWED_EXTENSIONS']

#import data processing package
import nltk
nltk.download('stopwords')
from bs4 import BeautifulSoup # For HTML parsing
import requests
import re # Regular expressions
from nltk.corpus import stopwords # Filter out stopwords, such as 'the', 'or', 'and'
import pandas as pd # For converting results to a dataframe and bar chart plots
from scipy import spatial
from bokeh.layouts import row
from bokeh.plotting import figure, show, output_file
from bokeh.embed import components
import numpy as np
from bokeh.layouts import row
from bokeh.plotting import figure, show, output_file
from bokeh.models import ColumnDataSource, LabelSet
from collections import Counter
from bokeh.io import hplot, output_file, show
from docx import Document
import re
import math
from time import sleep



def getText(filename):
    doc = docx.Document(filename)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    
    resume = '\n'.join(fullText)
    lines = [line.strip() for line in resume.splitlines()]
    chunks = [re.split('; |, |\*|\(|\)|\:| ',line) for line in lines]
    texts = []
    for chunk in chunks:
        texts = texts + chunk
    text_clean = [text.lower() for text in texts]
    doc_frequency = Counter() # This will create a full counter of our terms.
    doc_frequency.update(text_clean) # List comp
    my = Counter({'R':doc_frequency['r'], 'Python':doc_frequency['python'],
                 'Java':doc_frequency['java'], 'C++':doc_frequency['c++'],
                 'Ruby':doc_frequency['ruby'], 'Perl':doc_frequency['perl'],
                 'Matlab':doc_frequency['matlab'], 'JavaScript':doc_frequency['javascript'],
                 'Scala': doc_frequency['scala'],'Excel':doc_frequency['excel'],
                 'Tableau':doc_frequency['tableau'], 'D3.js':doc_frequency['d3.js'],
                 'SAS':doc_frequency['sas'], 'SPSS':doc_frequency['spss'],
                 'D3':doc_frequency['d3'], 'Hadoop':doc_frequency['hadoop'],
                 'MapReduce':doc_frequency['mapreduce'], 'Spark':doc_frequency['spark'],
                 'Pig':doc_frequency['pig'], 'Hive':doc_frequency['hive'],
                 'Shark':doc_frequency['shark'], 'Oozie':doc_frequency['oozie'],
                 'ZooKeeper':doc_frequency['zookeeper'], 'Flume':doc_frequency['flume'],
                 'Mahout':doc_frequency['mahout'], 'SQL':doc_frequency['sql'],
                 'NoSQL':doc_frequency['nosql'],'HBase':doc_frequency['hbase'],
                 'Cassandra':doc_frequency['cassandra'],'MongoDB':doc_frequency['mongodb']})
    my_df = pd.DataFrame(my,index=[0])
    my_df[my_df > 0]=1
    return my_df


def get_skills(website):
    '''
        This function just cleans up the raw html so that I can look at it.
        Inputs: a URL to investigate
        Outputs: Cleaned text only
        '''
    try:
        session_requests=requests.session()
        site=session_requests.get(website).content # Connect to the job posting
    except:
        return   # Need this in case the website isn't there anymore or some other weird connection problem
    
    soup_obj = BeautifulSoup(site) # Get the html from the site

    if len(soup_obj) == 0: # In case the default parser lxml doesn't work, try another one
        soup_obj = BeautifulSoup(site, 'html5lib')
    
    
    for script in soup_obj(["script", "style"]):
        script.extract() # Remove these two elements from the BS4 object
    
    text = soup_obj.get_text() # Get the text from this
    lines = [line.strip() for line in text.splitlines()] # break into lines
    chunks = [phrase.strip() for line in lines for phrase in line.split("  ")] # break multi-headlines into a line each
    text = ''.join(chunk for chunk in chunks if chunk).encode('utf-8') # Get rid of all blank lines and ends of line
    
    # Now clean out all of the unicode junk (this line works great!!!)
    try:
        text = text.decode(encoding = 'utf-8') # Need this as some websites aren't formatted
    except:                                                            # in a way that this works, can occasionally throw
        return                                                         # an exception

    text = re.sub("[^a-zA-Z+3]"," ", text)  # Now get rid of any terms that aren't words (include 3 for d3.js)
    # Also include + for C++
    text = re.sub(r"([a-z])([A-Z])", r"\1 \2", text) # Fix spacing issue from merged words
    text = text.lower().split()  # Go to lower case and split them apart
    stop_words = set(stopwords.words("english")) # Filter out any stop words
    text = [w for w in text if not w in stop_words]

    text = list(set(text)) # Last, just get the set of these. Ignore counts (we are just looking at whether a term existed
    # or not on the website)
    doc_frequency = Counter() # This will create a full counter of our terms.
    doc_frequency.update(text) # List comp
    #create dictionaries indicating skill set
    prog_lang_dict = Counter({'R':doc_frequency['r'], 'Python':doc_frequency['python'],
                             'Java':doc_frequency['java'], 'C++':doc_frequency['c++'],
                             'Ruby':doc_frequency['ruby'],
                             'Perl':doc_frequency['perl'], 'Matlab':doc_frequency['matlab'],
                             'JavaScript':doc_frequency['javascript'], 'Scala': doc_frequency['scala']})

    analysis_tool_dict = Counter({'Excel':doc_frequency['excel'],  'Tableau':doc_frequency['tableau'],
                             'D3.js':doc_frequency['d3.js'], 'SAS':doc_frequency['sas'],
                             'SPSS':doc_frequency['spss'], 'D3':doc_frequency['d3']})
    
    hadoop_dict = Counter({'Hadoop':doc_frequency['hadoop'], 'MapReduce':doc_frequency['mapreduce'],
                          'Spark':doc_frequency['spark'], 'Pig':doc_frequency['pig'],
                          'Hive':doc_frequency['hive'], 'Shark':doc_frequency['shark'],
                          'Oozie':doc_frequency['oozie'], 'ZooKeeper':doc_frequency['zookeeper'],
                          'Flume':doc_frequency['flume'], 'Mahout':doc_frequency['mahout']})
        
    database_dict = Counter({'SQL':doc_frequency['sql'], 'NoSQL':doc_frequency['nosql'],
                                                  'HBase':doc_frequency['hbase'], 'Cassandra':doc_frequency['cassandra'],
                                                  'MongoDB':doc_frequency['mongodb']})
    post_skills = prog_lang_dict.copy()
    post_skills.update(analysis_tool_dict)
    post_skills.update(hadoop_dict)
    post_skills.update(database_dict)
    post_df = pd.DataFrame(dict(post_skills),index = [0])

    return post_df



#define a function that gets skills count of a job post
@app_lulu.route('/')
def index():
    return render_template('index.html')

@app_lulu.route('/upload', methods=['POST'])
def upload():
    # Get the name of the uploaded file
    file = request.files['file']
    # Check if the file is one of the allowed types/extensions
    if file and allowed_file(file.filename):
        # Make the filename safe, remove unsupported chars
        filename = secure_filename(file.filename)
        # Move the file form the temporal folder to
        # the upload folder we setup
        file.save(os.path.join(app_lulu.config['UPLOAD_FOLDER'], filename))
        # Redirect the user to the uploaded_file route, which
        # will basicaly show on the browser the uploaded file
        global my_df
        my_df = getText(os.path.join(app_lulu.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('getlink')) #redirect to website where getlink gets executed




def post_info(city = None, state =None):
    
    final_job = 'data+scientist'
    
    if city is not None:
        final_city = city.split()
        final_city = '+'.join(word for word in final_city)
        final_site_list = ['http://www.indeed.com/jobs?q=%22', final_job, '%22&l=', final_city,
                           '%2C+', state] # Join all of our strings together so that indeed will search correctly
    else:
        final_site_list = ['http://www.indeed.com/jobs?q="', final_job, '"']
    
    final_site = ''.join(final_site_list)
    base_url = 'http://www.indeed.com'
    
    try:
        session_requests=requests.session()
        html =session_requests.get(final_site).content #open the job search page
    except:
        'That city/state combination did not have any jobs. Exiting'
        return
    soup = BeautifulSoup(html)

#Now find out how many jobs there were

    num_jobs_area = soup.find(id = 'searchCount').string.encode('utf-8')
    job_numbers = re.findall('\d+', str(num_jobs_area))
    
    if len(job_numbers) > 3:#Have a total number of jobs greater than 1000?
        total_num_jobs = (int(job_numbers[2])*1000) + int(job_numbers[3])
    else:
        total_num_jobs = int(job_numbers[2])
    city_title = city
    if city is None:
        city_title = 'Nationawide'
    print('There were', total_num_jobs, 'jobs found', city_title)
    
    num_pages = total_num_jobs/10 #know the total number of time we attempt search result page
    
    rank = []
    for i in range(1,5):#int(np.ceil(num_pages)+1)
        print('Getting page',i)
        start_num = str(i*10)
        current_page = ''.join([final_site,'&start=',start_num])
        session_requests=requests.session()
        html_page =session_requests.get(current_page).content #open the job search page
        page_obj = BeautifulSoup(html_page)
        job_link_area = page_obj.find(id = 'resultsCol') #Only the center area of the page
        
        job_URLS = [base_url + str(link.get('href')) for link in job_link_area.findAll('a')]
        job_URLS = list(filter(lambda x: 'clk' in x, job_URLS))
        
        for j in range(0, len(job_URLS)):
            final_description = get_skills(job_URLS[j])
            score = round(1 - spatial.distance.cosine(my_df,final_description),2)
            if math.isnan(score) is False:    #need to address nan website later, two situation: different formats, no skill match
                rank.append([job_URLS[j],float(score)])
            sleep(1)
    print('Done collecting job posts')
    rank = sorted(rank, key = lambda x: x[1], reverse = True)
    
    return rank
    #for i in range(len(rank)):
    #print('Top', i+1,':', rank[i][0],'   score:', rank[i][1])







app_lulu.vars={}

@app_lulu.route('/link',methods=['GET','POST'])
def getlink():
    if request.method == 'GET':
        return render_template('userinfo_lulu.html')
    else:
        #request was a POST
        app_lulu.vars['city'] = request.form['City']
        app_lulu.vars['state'] = request.form['State']
        rank = post_info(app_lulu.vars['city'], app_lulu.vars['state'])
        return render_template('table.html',pages = rank)



if __name__ == "__main__":
    app_lulu.run(debug=True)
