import pandas as pd
from datetime import date


def db_data_process(df):
    today = date.today()
    df['date'] = today.strftime("%d/%m/%Y")
    df['date'] = df['date'].astype('datetime64')


    df['days'] = (df['share_time'].str.extract(r'(\d+\s*\w+)')[0]
                              .replace({r'minutes?': '*1/1440',
                                        r'days?': '*1', 
                                        r'weeks?': '*7', 
                                        r'hours?': '*1/24', 
                                        r'months?': '*30',  
                                        r'years?': '*365'}, regex=True)
                              .apply(pd.eval))
    
    df["share_date"]=df["date"]-pd.to_timedelta(df["days"], unit='D')

    df['application_count'] = df.number_of_application.str.extract('(\d+)')
    df['application_count'] = df['application_count'].fillna(0)
    df['application_count'] = df['application_count'].astype(str).astype(int)

    df.drop(['share_time', 'date', 'days', 'number_of_application'], axis=1, inplace=True)

    return df



df = db_data_process(df=pd.read_csv("./data/data.csv"))
print(df.columns)  # ['title', 'company', 'location', 'jobDescription', 'share_date' , 'application_count']