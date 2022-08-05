# LinkedinJobAnalyzes
Creates a dashboard. allows you analyze Linkedin Job Postings!

### About The Project
With this project, log in to LinkedIn automatically with your user information on the dashboard prepared with streamlit. Then enter the Job title you want to analyze and the location to be analyzed. Bring the details of the job posting on as many pages as you want in this location and title as csv file. The data has been prepared for analysis and when you call the data, the plots will automatically be reflected on the screen.

#### About the data brought from LinkedIn
Columns: title, company, location, share_time, number_of_applcation, jobDescription

title: Job title to be analyzed

company: Company name that posted the job posting

location: Location of the job

share_time: About when the job posting was posted

number_of_applcation: Number of job applications up to share_time

jobDescription: Details about the job posting given by the job posting owner

### Built with
* Python (Selenium, BeautifulSoup, Pandas, Workcloud, NLTK, Matplotlib, Seaborn, Streamlit)

#### Usage
With ```pip install requirements.txt``` , you can install the modules and libraries used with their versions.

** Warning: Make sure your account language is English before running the code! 

You can run the code with ```streamlit run app.py``` 


<img src="project.gif" width="800" height="400"/>
