#!/usr/bin/env python
# coding: utf-8

# In[8]:


# Import necessary modules
import requests
from bs4 import BeautifulSoup
import pandas as pd


# In[2]:


# Set the URL to scrape
url = "https://www.imdb.com/search/title/?groups=top_100&sort=user_rating,desc"


# In[3]:


# Send an HTTP request to the URL and store the response
response = requests.get(url)


# In[4]:


# Parse the HTML content of the response
soup = BeautifulSoup(response.content, "html.parser")


# In[5]:


# Find all the <div> elements with the class "lister-item mode-advanced"
movies = soup.find_all('div', class_='lister-item mode-advanced')


# In[6]:


# For each movie, extract the title and rating
movie_name = []
Rating = []
for movie in movies:
    
    title = movie.h3.a.text
    movie_name.append(title)

    rating = movie.strong.text
    Rating.append(rating)


# In[9]:


# we will create a dictionary first, then turn this dictionary to the DataFrame, and see the top 5 elements of it.
dic = {"Movie Name" : movie_name, "Rating" : Rating}
df = pd.DataFrame(dic)
df.head(5)


# In[10]:


# we will repeat the process once again, but this time we will use another link because the link of the 51-100 is different.
movie_name_2 = []
Rating_2 = []

movie_name_2 = []
Rating_2 = []

import requests
from bs4 import BeautifulSoup

# Send an HTTP request to the URL of the webpage you want to access
url = "https://www.imdb.com/search/title/?groups=top_100&sort=user_rating,desc&start=51&ref_=adv_nxt"
page = requests.get(url)

# Parse the HTML content of the page
soup = BeautifulSoup(page.text, 'html.parser')

# Find all the <div> elements with the class "lister-item mode-advanced"
movies = soup.find_all('div', class_='lister-item mode-advanced')

# For each movie, extract the title and rating
for movie in movies:
    
    title = movie.h3.a.text
    movie_name_2.append(title)

    rating = movie.strong.text
    Rating_2.append(rating)

dic2 = {"Movie Name" : movie_name_2, "Rating" : Rating_2}
df2 = pd.DataFrame(dic2)
df2.head(5)


# In[14]:


# In the final step, we will merge two DataFrames, and here we have IMDB's top 100 movie list.
imdb_top_100 =  pd.concat([df, df2], axis=0)
imdb_top_100


# In[ ]:




