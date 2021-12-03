#!/usr/bin/env python
# coding: utf-8

# ## Logging on
# 
# Use Selenium to visit https://webapps1.chicago.gov/buildingrecords/ and accept the agreement.
# 
# > Think about when you use `.find_element...` and when you use `.find_elementSSS...`

# In[2]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd


# In[2]:


driver = webdriver.Chrome(ChromeDriverManager().install())


# In[3]:


driver.get('https://webapps1.chicago.gov/buildingrecords/')


# In[4]:


driver.find_element(By.ID, 'rbnAgreement1').click()


# In[5]:


driver.find_element(By.ID, 'submit').click()


# ## Searching
# 
# Search for **400 E 41ST ST**.

# In[6]:


driver.find_element(By.ID, 'fullAddress').send_keys('400 E 41ST ST')


# In[7]:


driver.find_element(By.ID, 'submit').click()


# ## Saving tables with pandas
# 
# Use pandas to save a CSV of all **permits** to `Permits - 400 E 41ST ST.csv`. Note that there are **different sections of the page**, not just one long permits table.
# 
# > - *Tip: When using `.read_html`, try using `flavor='lxml'` and comparing the results to `flavor='html5lib'`. Which works better?*
# > - *Tip: You might need to install `html5lib` using `pip`. If so, you'll need to restart the notebook using **Kernel > Restart** before it will work.*

# In[8]:


permit = driver.find_element(By.ID, 'resultstable_permits')
#df = pd.read_html(permit.get_attribute('outerHTML'), flavor='lxml')[0]
df = pd.read_html(permit.get_attribute('outerHTML'), flavor='html5lib')[0]
df
#'html5lib' works better because it can return all the date issued


# ## Saving tables the long way
# 
# Save a CSV of all DOB inspections to `Inspections - 400 E 41ST ST.csv`.
# 
# This is more complicated than the last one becuse **we also need to save the URL to the inspection** (see how the inspection number is a link?). As a result, you won't be able to use pandas! Instead, you'll need to use a loop and create a list of dictionaries.
# 
# You can use Selenium or you can feed the source to BeautifulSoup. You should have approximately 160 rows.
# 
# You'll probably need to find the table first, then the rows inside, then the cells inside of each row. You'll probably use lots of list indexing. I might recommend XPath for finding the table.
# 
# *Tip: If you get a "list index out of range" error, it's probably due to an issue involving `thead` vs `tbody` elements. What are they? What are they for? What's in them? There are a few ways to troubleshoot it.*

# In[9]:


inspections = driver.find_element(By.ID, 'resultstable_inspections')


# In[10]:


rows = inspections.find_elements(By.TAG_NAME, 'tr')
inspect_result = []
for row in rows[1:]:
    one_row = {}
    cells = row.find_elements(By.TAG_NAME, 'td')
    one_row['ID'] = cells[0].text
    one_row['Date'] = cells[1].text
    one_row['Status'] = cells[2].text
    one_row['Type_description'] = cells[3].text
    one_row['href'] = cells[0].find_element(By.TAG_NAME, 'a').get_attribute('href')
    inspect_result.append(one_row)
inspect_result


# In[11]:


df = pd.DataFrame(inspect_result)
df


# In[12]:


df.shape


# In[13]:


df.to_csv('Inspections - 400 E 41ST ST.csv', index=False)


# ### Bonus preview of Wednesday's content
# 
# **You prrrrrobably shouldn't do this one unless you want a real challenge.**
# 
# If you click the inspection number, it'll open up a new window that shows you details of the violations from that visit. Count the number of violations for each visit and save it in a new column called **num_violations**.
# 
# Save this file as `Inspections - 400 E 41ST ST - with counts.csv`.
# 
# Since clicking the link opens in a new window, we have to say "Hey Selenium, pay attention to that new window!" We do that with `driver.switch_to.window(driver.window_handles[-1])` (each window gets a `window_handle`, and we're just asking the driver to switch to the last one.). A rough sketch of what your code will look like is here:
# 
# ```python
# # Click the link that opens the new window
# 
# # Switch to the new window/tab
# driver.switch_to.window(driver.window_handles[-1])
# 
# # Do your scraping in here
# 
# # Close the new window/tab
# driver.close()
# 
# # Switch back to the original window/tab
# driver.switch_to.window(driver.window_handles[0])
# ```
# 
# You'll want to play around with them individually before you try it with the whole set - the ones that pass are very different pages than the ones with violations! There are a few ways to get the number of violations, some easier than others.

# In[14]:


#Method 1
inspections = driver.find_element(By.ID, 'resultstable_inspections')
rows = inspections.find_elements(By.TAG_NAME, 'tr')
list_violation = []
for row in rows[1:]:
        cells = row.find_elements(By.TAG_NAME, 'td')
        id_ = cells[0].text
        status = cells[2].text
        if status == 'FAILED':
            cells[0].click()
            driver.switch_to.window(driver.window_handles[-1])
            counts = driver.find_elements(By.TAG_NAME, 'tr')
            if len(counts) > 2:
                list_violation.append(len(counts) - 2)
            else:
                list_violation.append(0)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
        else:
            list_violation.append(0)


# In[15]:


df['num_violations'] = list_violation
df.head()


# In[16]:


df.to_csv("Inspections - 400 E 41ST ST - with counts.csv", index=False)


# In[ ]:





# In[16]:


#Method 2
import re

inspections = driver.find_element(By.ID, 'resultstable_inspections')
rows = inspections.find_elements(By.TAG_NAME, 'tr')
for row in rows[1:]:
    row.find_element(By.TAG_NAME, 'a').click()
    driver.switch_to.window(driver.window_handles[-1])
    try:
        number_result = driver.find_element_by_xpath("/html/body/div/div[4]/div[4]/div/div[2]/div").text
        number = re.findall(r' (\d+) entries', number_result)
        print(number)
    except:
        print('NaN')
    driver.close()
    driver.switch_to.window(driver.window_handles[0])


# In[21]:


#Method 3
inspections = driver.find_element(By.ID, 'resultstable_inspections')
rows = inspections.find_elements(By.TAG_NAME, 'tr')
for row in rows[1:]:
    row.find_element(By.TAG_NAME, 'a').click()
    driver.switch_to.window(driver.window_handles[-1])
    try:
        counts = driver.find_elements(By.TAG_NAME, 'tr')
        if len(counts) == 0:
            print(0)
        else:
            print(len(counts)-2)
    except:
        print('NaN')
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

