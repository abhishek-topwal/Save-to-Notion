from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

browser = webdriver.Firefox()

#open linkedIn
browser.get('http://www.linkedin.com/feed/')
# assert 'LinkedIn' in browser.title
cookies = browser.get_cookies()
[print(cookie) for cookie in cookies]


#find the search box
# elem = browser.find_element(By.ID, 'global-nav-search')  # Find the search box
# # elem = browser.find_element(By.NAME, 'p')  # Find the search box
# elem.send_keys('Abhishek Topwal' + Keys.RETURN)
# browser.quit()