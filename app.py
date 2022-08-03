import streamlit as st
from analyzer import LinkedinAnalyzer
import pandas as pd
from visualizations import states_most_number_of_jobs, top_five_title_max_number_job, top_five_company_related_job, work_cloud, most_occurent_important_words, average_job_applications
# Set page width to wide
st.set_page_config(layout='wide')

# Create sidebar
st.sidebar.markdown("<img src='https://pngimg.com/uploads/linkedIn/linkedIn_PNG38.png'  width=200 />", unsafe_allow_html=True)
st.sidebar.markdown("This dashboard allows you analyse Linkedin Job Postings!")
st.sidebar.markdown("To get started <ol><li>Enter the informations about job you wish to analyse</li> <li>Hit Get Data.</li> <li>Get analyzing</li></ol>",unsafe_allow_html=True)


# Input
email = st.text_input("Enter your gmail for login Linkedin: ", value="")
password = st.text_input("Enter your password for login Linkedin: ", value="")
position = st.text_input("Job position name to be analyzed: ", value="")
location =  st.text_input("The location of the job : ", value="")
number_of_pages = st.text_input("Number of pages to analyze : ", value="")

if st.button('Get Data'):
    analyzer = LinkedinAnalyzer(email=email, password=password)
    analyzer.run(maxPage=number_of_pages, position=position, local=location)
    df = pd.read_csv("./data/data.csv")
    df
    st.markdown('##')
    st.title('Analyzes')
    # Split columns
    left_col, mid_col, right_col = st.columns(3)
    # Viz ops
    states_most_number_of_jobs(df=df, left_col=left_col)   
    top_five_title_max_number_job(df=df, right_col=right_col)
    top_five_company_related_job(df=df, mid_col=mid_col)
    st.markdown('##')
    # Split columns
    second_left, second_right = st.columns(2)
    work_cloud(df=df, second_left=second_left)
    most_occurent_important_words(df=df, second_right=second_right)
    try:
        average_job_applications(df=df)
    except:
        pass
    
    
    