import streamlit as st
from wordcloud import WordCloud, STOPWORDS
from summary_jobs import Frequency
import itertools
import pandas as pd
from nltk.tokenize import word_tokenize

# import viz modules
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rcParams
from IPython.core.pylabtools import figsize

import nltk
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
nltk.download('stopwords')
nltk.download('punkt')

def states_most_number_of_jobs(df, left_col):
    rcParams['figure.figsize'] = 12,5

    from IPython.core.pylabtools import figsize

    fig, ax = plt.subplots(nrows=1, ncols=1)
    a = sns.barplot(x=df["location"].value_counts().index[:], y = df["location"].value_counts()[:])
    sns.despine(bottom = False, left = False)
    plt.title('\n States with Most Number of Jobs \n', size=16, color='black')
    plt.xticks(fontsize=13)
    plt.xticks(rotation=90)
    plt.yticks(fontsize=12)
    plt.xlabel('\n States \n', fontsize=13, color='black')
    plt.ylabel('\n Count \n', fontsize=13, color='black')
    left_col.pyplot(fig, use_container_width=True)
  
    

def top_five_company_related_job(df, mid_col):
    fig = plt.figure()
    my_explode=(0,0.1,0.1,0.1,0.1)
    labels= [x for x in df["company"].value_counts().sort_values(ascending=False)[0:5].index] # piechart for only top 5 company
    patches,ax, text= plt.pie(df["company"].value_counts().sort_values(ascending=False)[0:5],autopct='%1.1f%%',explode=my_explode,shadow=True,startangle=305)
    plt.title('\n Top 5 Company with Most Number of Related Job \n', size=16, color='black')
    plt.legend(patches, labels, loc="best")
    plt.axis('equal')
    mid_col.pyplot(fig, use_container_width=True)


def top_five_title_max_number_job(df, right_col):
    fig, ax = plt.subplots(nrows=1, ncols=1)
    a = sns.barplot(x= df["title"].value_counts().sort_values(ascending=False).head(5).index ,y= df["title"].value_counts().sort_values(ascending=False).head(5))
    #Removing top and Right borders
    sns.despine(bottom = False, left = False)
    #Beautifying the plot
    plt.title('\n Top 5 title with Maximum Number of Job Postings \n', size=16, color='black')
    plt.xticks(fontsize=13,rotation=90)
    plt.yticks(fontsize=12)
    plt.xlabel('\n Title \n', fontsize=13, color='black')
    plt.ylabel('\n Count \n', fontsize=13, color='black')
    right_col.pyplot(fig, use_container_width=True)
    
    
def work_cloud(df, second_left):
    rcParams['figure.figsize'] = 12,5
    aggregate_descriptions = " ".join(job_description.lower() 
                      for job_description in df.jobDescription)
   
    f = Frequency()
    stopwords = f.stopwords
    wordcloud = WordCloud(stopwords=stopwords, background_color='white',
                         width=1000, height=700).generate(aggregate_descriptions)
    fig = plt.figure()
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    second_left.pyplot(fig)
    
    
def most_occurent_important_words(df, second_right):
    rcParams['figure.figsize'] = 12,5
    f = Frequency()
    stops = f.stopwords
    summary_words = df.jobDescription.map(lambda desc: set(
    word_tokenize(
        " ".join(
            Frequency().summarize(desc.replace(".", ". ").replace("•", " "), 2)
        )
    )
    ) -stops)
    # non_summary = pd.Series(list(itertools.chain.from_iterable(non_summary_words.values)))
    fig = plt.figure()
    summary = pd.Series(list(itertools.chain.from_iterable(summary_words.values)))
    sns.set_style("white")
    summary.value_counts(ascending=False).head(12).plot.bar(fontsize=16, figsize=(14, 6))
    second_right.pyplot(fig)
    
    
def average_job_applications(df):
    # English
    df['numeric_share_time(day)'] = (df['share_time'].str.extract(r'(\d+\s*\w+)')[0]
                              .replace({r'minutes?': '*1/1440',
                                        r'days?': '*1', 
                                        r'weeks?': '*7', 
                                        r'hours?': '*1/24', 
                                        r'months?': '*30',  
                                        r'years?': '*365'}, regex=True)
                              .apply(pd.eval)
               )
    df['numeric_share_time(day)'] = df['numeric_share_time(day)'].round(3)
    df['number_of_application_numeric'] = df['number_of_application'].str.replace('applicant', '')
    df['number_of_application_numeric'] = df['number_of_application'].str.replace('applicants', '')
    df['number_of_application_numeric'] = df['number_of_application_numeric'].str.replace('Over', '')
    df["number_of_application_numeric"]  = pd.to_numeric(df['number_of_application_numeric'])
    
    # Fist df (ALL Data)
    df_number_app = df[["number_of_application_numeric"]]
    
    # Second df (Just last 1 week)
    df_one_week = df[['numeric_share_time(day)', 'number_of_application_numeric']]
    df_one_week['numeric_share_time(day)'] = pd.to_numeric(df_one_week ['numeric_share_time(day)'])
    df_one_week['mean_aplication_last_one_week'] = pd.to_numeric(df_one_week ['number_of_application_numeric'])
    df_one_week= df_one_week[df_one_week['numeric_share_time(day)'] <8]
    df_one_week = df_one_week.reset_index(drop=True)
    df_number_app_one_week = df_one_week[["mean_aplication_last_one_week"]]
    
    fig = plt.figure()
    plt.bar(df_number_app.mean(), align='edge', height=0.5, width=-0.3, label='Average number of job applications in the postings')
    plt.bar(df_number_app_one_week.mean(), align='edge', height=0.5, width=0.3, label='Average number of job applications in the last 1 week in the postings')
    plt.yticks([])
    plt.legend()
    st.pyplot(fig)