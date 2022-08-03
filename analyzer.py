import os
import re
from pathlib import Path
from time import sleep
from urllib.parse import unquote
import logging

import pandas as pd
from bs4 import BeautifulSoup
from parsel import Selector
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from unidecode import unidecode
from webdriver_manager.chrome import ChromeDriverManager


class LinkedinAnalyzer:
    def __init__(self, email, password):
        log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        logging.basicConfig(level=logging.INFO, format=log_fmt)
        logging.info("Starting Driver!")
        self.email = email
        self.password = password
    
    def login(self):
        """
        Automatically login to LinkedIn account and return driver
        """
        try:
            logging.info("Logging in")
            # Prevents version errors between chrom and chrom-driver
            service=Service(ChromeDriverManager().install())
            # Detirmine tour driver
            driver = webdriver.Chrome(service=service)
            driver.maximize_window()
            # Get linkedin Login Page
            driver.get('https://www.linkedin.com/login/tr')
            # Fill username and password sections with user informations
            email = driver.find_element("xpath", ".//input[@name='session_key' and @type='text']")
            email.send_keys(self.email)
            password = driver.find_element("xpath", ".//input[@type='password']")
            password.send_keys(self.password)
            # login button
            driver.find_element("xpath", "//button[@class='btn__primary--large from__button--floating']").click()
            sleep(3)
            return driver
    
        except Exception as e:
            print(e)

    def jobInformation(self, driver):
        """
        in the job posting
        Scrapes title, company location, share time and job Description properties from the source page 
        """
        
        logging.info("Get informations")
        title = ''
        company = ''
        location = ''
        share_time =''
        jobDescription = ''
        # Get page source
        html = driver.page_source
        soup = BeautifulSoup(html, features="html.parser")
        sel = Selector(text=html)
        # Get informations about jobs(Job title, company name, jon location, number of application, job description)
        try:
            title = soup.find("h2", {"class": "t-24 t-bold jobs-unified-top-card__job-title"}).text
        except:
            pass
        try:
            company = "".join((soup.find("span", {"class": "jobs-unified-top-card__company-name"}).text).split())
        except:
            pass
        try:
            location = "".join((soup.find("span", {"class": "jobs-unified-top-card__bullet"}).text).split())
        except:
            pass
        try: 
            share_time = "".join((soup.find("span", {"class": "jobs-unified-top-card__subtitle-secondary-grouping t-black--light"}).text).split())
        except:
            pass
        try:
            jobDescription = sel.xpath('//*[@id="job-details"]').extract()
            jobDescription = BeautifulSoup(jobDescription,features='html.parser').text
            jobDescription= re.sub('<[^<]+?>', '', jobDescription[0])
        except:
            pass
        
        # List collected information
        l = [title, company, location, share_time,  jobDescription]
        # Remove components such as tags in jobDescription
        l[4][0] = re.sub('<[^<]+?>', '', l[4][0])
        return l

    def getAllJobInfo(self, driver, maxPage, position: str, local: str):
        """
        Args:
            driver : login() 
            maxPage : Number of pages for the information to scraping
            position : Position name to be analyzed
            local: The location where the determined job position will be analyzed 
        """
        maxPage = int(maxPage)
        logging.info("Search and collect information from jobs page")
        actions = ActionChains(driver=driver)
        data = [["title", "company", "location", "share_time" , "jobDescription"]]
        # Go jobs section
        position = unquote(unidecode(position))
        local = unquote(unidecode(local))
        # formating to linkedin model
        position = position.replace(' ', "%20")
        for p in range(maxPage):
            page = str(p*25)
            driver.get(f"https://www.linkedin.com/jobs/search/?&keywords={position}&location={local}&start={page}")
            sleep(3)
            jobs = driver.find_elements(By.CLASS_NAME,'jobs-search-results__list-item')
            for j in jobs:
                sleep(3)
                actions.move_to_element(j).perform()
                j.find_element(By.TAG_NAME,'img').click()
                sleep(3)
                data.append(self.jobInformation(driver))
        df = pd.DataFrame(data[1:],columns=data[0])
        df.to_csv('results.csv')
        
    
    def data_processing(self, df: pd.DataFrame):
        """
        Prepare data for analysis
        Args:
            df (pd.DataFrame): Dataframe created from scraped data
        """
        logging.info("Preapere dataframe for analyzes!")
        # Create a path for prepared data frame
        Path(f"./data/").mkdir(parents=True, exist_ok=True)
        # Drop unnecessary columns in dataframe
        if 'Unnamed: 0' in df.columns:
            df = df.drop('Unnamed: 0', axis=1)
        # Delete "\n", "[", "\u", "]" characters from jobDescription column
        df['jobDescription'] = df['jobDescription'].replace(r'\s+|\\n', ' ', regex=True) 
        df['jobDescription'] = df['jobDescription'].replace(r'\s+|\\u', ' ', regex=True) 
        df["jobDescription"] = df["jobDescription"].str.replace("^\[.|.\]$","", regex=True)
        # Split the share_time column into 2 columns after "ago"(share_time', 'number_of_application)
        df[['share_time', 'number_of_application']] = df['share_time'].str.split('ago', 1, expand=True)
        # Change order of columns
        df = df[['title', 'company', 'location', 'share_time', 'number_of_application', 'jobDescription']]
        # Save the prepared dataframe
        output_file = os.path.join('./data','data.csv')
        df.to_csv(output_file, index=False)
    
    def run(self, maxPage, position, local):
        """ 
        Run LinkedinAnalyzer! Login LinkedIn, collect data, correct and prepare for analysis
        """
        driver = self.login()
        df = self.getAllJobInfo(driver=driver, maxPage=maxPage, position=position, local=local)
        self.data_processing(df=pd.read_csv('results.csv'))
        logging.info("Done scraping.")
