#!/usr/bin/env python
# coding: utf-8

# # Scraping basics for Selenium
# 
# If you feel comfortable with scraping, you're free to skip this notebook.

# ## Part 0: Imports
# 
# Import what you need to use Selenium, and start up a new Chrome to use for scraping. You might want to copy from the [Selenium snippets](http://jonathansoma.com/lede/foundations-2018/classes/selenium/selenium-snippets/) page.
# 
# **You only need to do `driver = webdriver.Chrome(...)` once,** every time you do it you'll open a new Chrome instance. You'll only need to run it again if you close the window (or want another Chrome, for some reason).

# In[1]:


from selenium import webdriver
from selenium.webdriver.common.by import By

from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd


# In[2]:


driver = webdriver.Chrome(ChromeDriverManager().install())


# ## Part 1: Scraping by class
# 
# Scrape the content at http://jonathansoma.com/lede/static/by-class.html, printing out the title, subhead, and byline.

# In[3]:


driver.get('https://jonathansoma.com/lede/static/by-class.html')


# In[4]:


driver.find_element(By.CLASS_NAME, 'title').text


# In[5]:


driver.find_element(By.CLASS_NAME, 'subhead').text


# In[6]:


driver.find_element(By.CLASS_NAME, 'byline').text


# ## Part 2: Scraping using tags
# 
# Scrape the content at http://jonathansoma.com/lede/static/by-tag.html, printing out the title, subhead, and byline.

# In[7]:


driver.get('http://jonathansoma.com/lede/static/by-tag.html')


# In[8]:


driver.find_element(By.TAG_NAME, 'h1').text


# In[9]:


driver.find_element(By.TAG_NAME, 'h3').text


# In[10]:


driver.find_element(By.TAG_NAME, 'p').text


# ## Part 3: Scraping using a single tag
# 
# Scrape the content at http://jonathansoma.com/lede/static/by-list.html, printing out the title, subhead, and byline.
# 
# > **This will be important for the next few:** if you scrape multiples, you have a list. Even though it's Seleninum, you can use things like `[0]`, `[1]`, `[-1]` etc just like you would for a normal list.

# In[11]:


driver.get('http://jonathansoma.com/lede/static/by-list.html')


# In[12]:


driver.find_elements(By.TAG_NAME, 'p')[0].text


# In[13]:


driver.find_elements(By.TAG_NAME, 'p')[1].text


# In[14]:


driver.find_elements(By.TAG_NAME, 'p')[-1].text


# ## Part 4: Scraping a single table row
# 
# Scrape the content at http://jonathansoma.com/lede/static/single-table-row.html, printing out the title, subhead, and byline.

# In[15]:


driver.get('http://jonathansoma.com/lede/static/single-table-row.html')


# In[16]:


driver.find_element(By.TAG_NAME, 'table').text


# In[17]:


driver.find_elements(By.TAG_NAME, 'td')[0].text


# In[18]:


driver.find_elements(By.TAG_NAME, 'td')[1].text


# In[19]:


driver.find_elements(By.TAG_NAME, 'td')[2].text


# ## Part 5: Saving into a dictionary
# 
# Scrape the content at http://jonathansoma.com/lede/static/single-table-row.html, saving the title, subhead, and byline into a single dictionary called `book`.
# 
# > Don't use pandas for this one!

# In[20]:


keys = ['title', 'subhead', 'byline']
contents = driver.find_elements(By.TAG_NAME, 'td')
values = [content.text for content in contents]
book = dict(zip(keys,values))
book


# ## Part 6: Scraping multiple table rows
# 
# Scrape the content at http://jonathansoma.com/lede/static/multiple-table-rows.html, printing out each title, subhead, and byline.
# 
# > You won't use pandas for this one, either!

# In[21]:


driver.get('http://jonathansoma.com/lede/static/multiple-table-rows.html')


# In[22]:


tds = driver.find_elements(By.TAG_NAME, 'td')
for td in tds:
    print(td.text)


# ## Part 7: Scraping an actual table
# 
# Scrape the content at http://jonathansoma.com/lede/static/the-actual-table.html, creating a list of dictionaries.
# 
# > Don't use pandas here, either!

# In[23]:


driver.get('http://jonathansoma.com/lede/static/the-actual-table.html')


# In[24]:


dataset = []
contents = driver.find_elements(By.TAG_NAME, 'tr')
for content in contents:
    book = {}
    book['title'] = content.find_elements(By.TAG_NAME, 'td')[0].text
    book['subhead'] = content.find_elements(By.TAG_NAME, 'td')[1].text
    book['byline'] = content.find_elements(By.TAG_NAME, 'td')[2].text
    dataset.append(book)
dataset


# In[ ]:





# ## Part 8: Scraping multiple table rows into a list of dictionaries
# 
# Scrape the content at http://jonathansoma.com/lede/static/the-actual-table.html, creating a pandas DataFrame.
# 
# > There are two ways to do this one! One uses just pandas, the other one uses the result from Part 7.

# In[25]:


# Method1: using the result from Part7
df = pd.DataFrame(dataset)
df


# In[26]:


# Method2: just using pandas
table = driver.find_element(By.ID, 'booklist')
pd.read_html(table.get_attribute('outerHTML'))[0]


# ## Part 9: Scraping into a file
# 
# Scrape the content at http://jonathansoma.com/lede/static/the-actual-table.html and save it as `output.csv`

# In[27]:


df.to_csv('output.csv', index=False)

