from flask import Flask,render_template,request,redirect
app_lulu = Flask(__name__)


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

def my_df():
    my_dict = {'R':1, 'Python':1,
    'Java':0, 'C++':0,
        'Ruby':0,
            'Perl':0, 'Matlab':0,
                'JavaScript':0, 'Scala': 0, 'Excel':1,  'Tableau':1,
    'D3.js':0, 'SAS':1,
        'SPSS':1, 'D3':0, 'Hadoop':0, 'MapReduce':1,
    'Spark':1, 'Pig':0,
        'Hive':0, 'Shark':0,
            'Oozie':0, 'ZooKeeper':0,
                'Flume':0, 'Mahout':0, 'SQL':1, 'NoSQL':0,
    'HBase':0, 'Cassandra':0,
        'MongoDB':0}

    my_df = pd.DataFrame(my_dict, index = [0])
    return my_df

app_lulu.vars={}

@app_lulu.route('/',methods=['GET','POST'])
def index_lulu():
    if request.method == 'GET':
        return render_template('userinfo_lulu.html')
    else:
        #request was a POST
        app_lulu.vars['post1'] = request.form['post1_lulu']
        app_lulu.vars['post2'] = request.form['post2_lulu']
        app_lulu.vars['post3'] = request.form['post3_lulu']
        app_lulu.vars['post4'] = request.form['post4_lulu']
        app_lulu.vars['post5'] = request.form['post5_lulu']
        
        my_df2 = my_df().transpose()
        my_array = np.array((my_df2[my_df2[0]==1].index))

        skills_required = []
        skills_have = []
        scores = []
        for web in app_lulu.vars.values():
            df = get_skills(web)
            score = 1 - spatial.distance.cosine(my_df(),df)
            df1 = df.transpose()
            skill_required = len(np.array((df1[df1[0]==1].index)))
            skill_have =len(list(filter(lambda x: x in my_array, np.array(df1[df1[0]==1].index))))
            skills_required.append(skill_required)
            skills_have.append(skill_have)
            scores.append(score)
        

        score_df = pd.DataFrame({'JobPost':list(app_lulu.vars.keys()), 'Matchness':scores,'Skills_Required':skills_required,'Skills_Have':skills_have})
        best_match = score_df[score_df['Matchness'] == score_df['Matchness'].max()]
        JobPost_num = best_match['JobPost'].values[0]
        matchness_per = best_match['Matchness'].values[0]
        
        factors = list(app_lulu.vars.keys())
        x = scores

        dot = figure(title="Job Matchness", tools="", toolbar_location=None,
             y_range=factors, x_range=[0,1], x_axis_label = 'Matchness', y_axis_label = 'JobPost')

        dot.segment(0, factors, x, factors, line_width=5, line_color="green", )
        dot.circle(x, factors, size=15, fill_color="orange", line_color="green", line_width=3, )
        script, div = components(dot)

        p = figure(title = "Skills Matchness")
        p.xaxis.axis_label = 'Skills Required'
        p.yaxis.axis_label = 'Skills Have'

        p.circle(score_df["Skills_Required"], score_df["Skills_Have"],
          fill_alpha=0.2, size=10)

        source = ColumnDataSource(score_df)

        labels = LabelSet(x="Skills_Required", y="Skills_Have", text="JobPost", y_offset=8,
                  text_font_size="8pt", text_color="#555555",
                  source=source, text_align='center')
        p.add_layout(labels)
        script2, div2 = components(p)


        return render_template('graph.html', script=script, div=div, div2=div2, num = JobPost_num)




if __name__ == "__main__":
    app_lulu.run(debug=True)
