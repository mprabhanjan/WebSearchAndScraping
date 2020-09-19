from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
#import random
from selenium.webdriver.common.action_chains import ActionChains
import pprint
from collections import defaultdict
import requests
from bs4 import BeautifulSoup

ChromeDriverLocation = "/Users/prabhanj/Downloads/chromedriver"
job_site = "https://jobs.paloaltonetworks.com/job-search-results/"
navig_xpath='//*[@id="widget-jobsearch-results-pages"]/a'

def getJobSearchResults(browser, job_site):
    browser.get(job_site)
    elem = browser.find_element_by_id("cws_jobsearch_keywords")
    #elem.send_keys("prisma cloud")
    elem.send_keys("")
    elem = browser.find_element_by_id("cws_jobsearch_multiCategory")
    elem.send_keys("Engineering")
    elem = browser.find_element_by_id("cws_jobsearch_compliment")
    elem.send_keys("Americas")
    elem = browser.find_element_by_id("cws_jobsearch_location")
    elem.send_keys("Santa Clara")
    elem = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "here-vicinity")))
    elem.click()

    elem = browser.find_element_by_id("cws-adv-search-btn")
    ac = ActionChains(browser)
    ac.move_to_element(elem).move_by_offset(60, 33).click().perform()
    time.sleep(1)

    job_urls = list()
    more_pages = True
    pageCount = 1
    while (more_pages):
        more_pages = False
        page_urls = list()
        job_classes = browser.find_elements_by_class_name('jobTitle')
        for jc in job_classes:
            link = jc.find_element_by_css_selector('a').get_attribute('href')
            page_urls.append(link)

        #pp = pprint.PrettyPrinter()
        #pp.pprint("====================================")
        #pp.pprint(page_urls)
        job_urls = job_urls + page_urls

        navig_parent = browser.find_element_by_id("widget-jobsearch-results-pages")
        navigation_elems = navig_parent.find_elements_by_css_selector('a')
        if len(navigation_elems) >= 2:
            elm = navigation_elems[-2]
            link_label = elm.get_attribute("aria-label")
            #print(link_label)
            if link_label.lower().startswith("go to the next page of results"):
                next_page_link = elm.get_attribute('href')
                pageCount += 1
                next_page = getNextPageLink(next_page_link, pageCount)
                #print("Next page at : %s" %(next_page))
                browser.get(next_page)
                time.sleep(1)
                more_pages = True
        '''
        navigation_elements = browser.find_elements_by_xpath(navig_xpath)
        if len(navigation_elements) >= 2:
            navig_elem = navigation_elements[-2]
            if navig_elem.text == '>':
                ac = ActionChains(browser)
                ac.move_to_element(navig_elem).move_by_offset(21, 20).click().perform()
                more_pages = True
                time.sleep(1)
        '''


    #time.sleep(2000)
    return job_urls

def getNextPageLink(link, nextPageCount):
    newLink = link[:-1] + "&pg=" + str(nextPageCount)
    return newLink

JobsOfInterest = defaultdict(list)
def searchKeyWordsInUrlSerenium(browser, url, key_words_list):
    browser.get(url)
    text = browser.page_source
    for key in key_words_list:
        if key in text:
            JobsOfInterest[key].append(url)


def searchKeyWordsinUrlBS4(url, key_words_list):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, 'html.parser')
    page_text = soup.get_text()
    for key in key_words_list:
        if key in page_text:
            JobsOfInterest[key].append(url)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    browser = webdriver.Chrome(ChromeDriverLocation)
    urls = getJobSearchResults(browser, job_site)
    pp = pprint.PrettyPrinter()
    pp.pprint("Found total %d results ::" %(len(urls)))
    #pp.pprint(urls)

    for url in urls:
        searchKeyWordsinUrlBS4(url, ["Go ", "GoLang ", "Java "])

    pp.pprint(JobsOfInterest)
    browser.close()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/

#x2='//*[@id="widget-jobsearch-results-pages"]/a[7]'


#https://jobs.paloaltonetworks.com/job-search-results/?keyword=prisma%20cloud&category[]=Engineering&compliment=Americas&location=Santa%20Clara%2C%20CA%2C%20USA&latitude=37.3541079&longitude=-121.9552356&radius=25&pg=2#
#https://jobs.paloaltonetworks.com/job-search-results/?keyword=prisma%20cloud&category[]=Engineering&compliment=Americas&location=Santa%20Clara%2C%20CA%2C%20USA&latitude=37.3541079&longitude=-121.9552356&radius=25&pg=2#
#https://jobs.paloaltonetworks.com/job-search-results/?keyword=prisma%20cloud&category[]=Engineering&compliment=Americas&location=Santa%20Clara%2C%20CA%2C%20USA&latitude=37.3541079&longitude=-121.9552356&radius=25&pg=2#
#next_page_linkhttps://jobs.paloaltonetworks.com/job-search-results/?keyword=prisma%20cloud&category[]=Engineering&compliment=Americas&location=Santa%20Clara%2C%20CA%2C%20USA&latitude=37.3541079&longitude=-121.9552356&radius=25&pg=2#
#https://jobs.paloaltonetworks.com/job-search-results/?keyword=prisma%20cloud&category[]=Engineering&compliment=Americas&location=Santa%20Clara%2C%20CA%2C%20USA&latitude=37.3541079&longitude=-121.9552356&radius=25&pg=3#
#https://jobs.paloaltonetworks.com/job-search-results/?keyword=prisma%20cloud&category[]=Engineering&compliment=Americas&location=Santa%20Clara%2C%20CA%2C%20USA&latitude=37.3541079&longitude=-121.9552356&radius=25#