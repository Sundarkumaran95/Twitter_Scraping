from pymongo import MongoClient
import snscrape.modules.twitter as sntwitter
import pandas as pd
import datetime as datetime
import streamlit as st
import json

Header = st.container()

with Header:
    st.title("Twitter Scraping application")
    st.text("Scraper for social networking platforms, \nby scraping things like user profiles, hashtags, or searches.")

with st.sidebar.form("Twitter_Scrapping"):
    from_keyword = st.text_input("Enter a keyword or an hashtag")
 # Input dates
    start = st.date_input("Enter the date start value", datetime.date(2022,1,1))
    end = st.date_input("Enter the date end value", datetime.date(2023,1,1))
    limit = st.number_input("Number of tweets to be fetched",0,1000)
    submitted1 = st.form_submit_button(label = 'Search Twitter 🔎')




# Scraping the data
list = []
for i,tweet in enumerate(sntwitter.TwitterSearchScraper(from_keyword + " until:" +str(end) + " since:" +str(start)).get_items()):
  if i > limit:
           break
    
  list.append([tweet.date,tweet.user.id,tweet.url,tweet.content,tweet.renderedContent,tweet.user.username,tweet.replyCount,tweet.retweetCount,tweet.lang,tweet.source,tweet.likeCount])
df = pd.DataFrame(list, columns = ['Date','ID','URL','Tweet','Content','User','Reply Count','Retweet Count','Language', 'Source','Like Count'])
submit = print(df)
st.dataframe(df)
       

# storing data in a database    
if st.button("Upload_to_database"):
   client = MongoClient("mongodb://localhost:27017")
   data=df.to_dict(orient="records")
   db=client["TwitterScrapping"]
   db.twitter.insert_many(data)
     
     
# saving the scrapped data into csv file         
   csv = df.to_csv()
   st.download_button("Download data as CSV",csv,file_name='Twitterscraped.csv')

# saving the scrapped data into json file
   json_file = df.to_json()
   st.download_button("Download data as json",json_file,file_name='Twitterscraped.json')
