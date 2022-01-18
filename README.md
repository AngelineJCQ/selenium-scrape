# Selenium: Scrape a dynamic webpage
 It's time to learn scrape and create my original data set. The package I use here is **Selenium**. It can simulate the actions of humans when browsing the web, such as clicking, turning pages, and entering query values. 

 Some of the function is similar to **Beautiful Soup**, another useful package for scraping. 

 The difference here is that:

 **Selenium** can be used in both static and dynamic. But it's less efficient and takes more time to get content from a static page.

 **Beautiful Soup** can only be used in static website. It can't interactive with the page, such as click or browse. But when fetching the content from a single page, it's more efficient.

## Part One: A Cheat Sheet

The notebook I use here is [0-basic-selenium.ipynb](https://github.com/AngelineJCQ/selenium-scrape/blob/main/0-basic-selenium.ipynb).

The cheat sheet includes:
- the basic imports
- scraping by class/tags/single tag
- scraping a single table row
- saving the scraping result into a dictionary
- scraping multiple table rows
- scraping an actual table
- saving the scraping result into a local file called [output.csv](https://github.com/AngelineJCQ/selenium-scrape/blob/main/output.csv)

## Part Two: Texas License Violations

In this case, I try to search for cosmetologist violations for people with the last name Nguyen in [Texas License Violations](https://www.tdlr.texas.gov/cimsfo/fosearch.asp).

The notebook I use here is [1-Texas-violation-scrape.ipynb](https://github.com/AngelineJCQ/selenium-scrape/blob/main/1-Texas-violation-scrape.ipynb).


The code includes:
- select a specific item from a drop-down list in a webpage
- scrape the result page and save it to a data frame
- save it as [output_violations.csv](https://github.com/AngelineJCQ/selenium-scrape/blob/main/output_violation.csv)


## Part Three: Chicago Building Inspection

In this case, the webpage I ask Selenium to visit is [Chicago Building Records](https://webapps1.chicago.gov/buildingrecords/).

The notebook I use here is [2-Chicago-building-scrape.ipynb](https://github.com/AngelineJCQ/selenium-scrape/blob/main/2-Chicago-building-scrape.ipynb).


The code includes:
- click many buttons to log in the website
- search for certain address: 400 E 41ST ST.
- save tables with pandas as [Inspections - 400 E 41ST ST.csv](https://github.com/AngelineJCQ/selenium-scrape/blob/main/Inspections%20-%20400%20E%2041ST%20ST.csv)
- click each inspection, go to the new window/tab, do scrape, close the new window/tab and switch back to the original window/tab
- save the result as [Inspections - 400 E 41ST ST - with counts.csv](https://github.com/AngelineJCQ/selenium-scrape/blob/main/Inspections%20-%20400%20E%2041ST%20ST%20-%20with%20counts.csv)

