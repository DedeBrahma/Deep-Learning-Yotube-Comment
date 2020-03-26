from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import re
import csv

driver = webdriver.Chrome("chromedriver.exe")
driver.get("https://www.youtube.com/watch?v=QJzSJhM9blI")
time.sleep(2)  # give the page some time to load

# --------------- FETCH TITLE ---------------
# get the video's title
title = driver.find_element_by_xpath('//*[@id="container"]/h1/yt-formatted-string').text
print(title)

# --------------- LOAD ALL COMMENTS ---------------
# defining the numbers here so we can reference and easily change them
SCROLL_PAUSE_TIME = 2
CYCLES = 100

# we know there's always exactly one HTML element, so let's access it
html = driver.find_element_by_tag_name('html')
# first time needs to not jump to the very end in order to start
html.send_keys(Keys.PAGE_DOWN)  # doing it twice for good measure
html.send_keys(Keys.PAGE_DOWN)  # one time sometimes wasn't enough
# adding extra time for initial comments to load
# if they fail (because too little time allowed), the whole script breaks
time.sleep(SCROLL_PAUSE_TIME * 3)
# and now for loading the hidden comments by scrolling down and up
for i in range(CYCLES):
    html.send_keys(Keys.END)
    time.sleep(SCROLL_PAUSE_TIME)
    # might not be necessary; try out without it.
    # html.send_keys(Keys.PAGE_UP)
    # time.sleep(SCROLL_PAUSE_TIME)


# --------------- GETTING THE COMMENT TEXTS ---------------
name_elems=driver.find_elements_by_xpath('//*[@id="author-text"]')
comment_elems = driver.find_elements_by_xpath('//*[@id="content-text"]')
num_of_names = len(name_elems)



# --------------- WRITING TO OUTPUT FILE ---------------
with open("ytb_comment.csv", "w", newline='', encoding='utf-8') as f:
    writer = csv.writer(f, delimiter=',')
    writer.writerow(['Username', 'Comment'])
    for i in range(num_of_names):
        name = name_elems[i].text
        text = comment_elems[i].text
        text = str(text).replace('\n', '')

        # writer.writerow(['Username', 'Comment'])
        writer.writerow([name, text])

driver.close()