from selenium import webdriver
import time
import random

ChromeDriverLocation = "/Users/prabhanj/Downloads/chromedriver"
whitney_web_site = "https://www.recreation.gov/permits/233260"
xpath = '//*[@id="division-selection"]/option[1]'

xpath_select_entry_point = '//*[@id="division-selection-label"]'

xpath_overnight = '//*[@id="division-selection"]/option[2]'
xpath_day_use = '//*[@id="division-selection"]/option[3]'
xpath_group_members = '//*[@id="number-input-"]'
xpath_group_members = '/html/body/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div/div/div/div[1]/div/div[2]/div[3]/div[1]/div/div/label'

full_path_day_use = '/html/body/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div/div/div/div[1]/div/div[2]/div[2]/div[2]/div/select/option[3]'
full_path_overnight = '/html/body/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div/div/div/div[1]/div/div[2]/div[2]/div[2]/div/select/option[2]'


def CheckWebsiteForEntryPoint(brower, xpath, entry_point, debug = False):

    result = list()
    try:
        elem = browser.find_element_by_xpath(xpath)
        if debug:
            print('    Found elem for %s Selection' %(entry_point))
        elem.click()
        time.sleep(random.randint(5000, 30000)/10000)
    except:
        if debug:
            print("    Unable to find the element for %s Selection!"%(entry_point))
        #browser.close()
        #time.sleep(random.randint(30, 60))
        return [(0, "     Entry-point element not found!")]

    try:
        time.sleep(1)
        elem = browser.find_element_by_id("number-input-")
        if debug:
            print("    Found elem for group_members!")
        for i in range (1, 16):
            val = str(i)
            elem.clear()
            time.sleep(1)
            elem.send_keys(val)
            elems = browser.find_elements_by_class_name("CalendarDay")
            #print("Number of Calendar Days %d" %(len(elems)))
            for e in elems:
                status = e.get_attribute("aria-label")
                if not status.lower().startswith("not available"):
                    print(status)
                    result.append((i, status))
                    #return (i, status)
        elem.clear()

    except:
        if debug:
            print("    Unable to find elem for group_members!")
        #browser.close()
        #time.sleep(random.randint(30, 60))
        return [(0, "    group_numbes element not found!")]

    #browser.close()
    return result

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    browser = webdriver.Chrome(ChromeDriverLocation)
    browser.get(whitney_web_site)
    for i in range(100):
        print("Starting Iteration %d ...."%(i))
        for entry_type, xpath in [("Day-Use", full_path_day_use), ("Overnight", full_path_overnight)]:

            result = CheckWebsiteForEntryPoint(browser, xpath, entry_type)
            for count, status in result:
                if count:
                    print("%s:: Count %d,  Status %s" %(entry_type, count, status))
                time.sleep(random.randint(2, 8))

        # browser.close()
        sleep_time = 30 + random.randint(0, 30)
        print("  Sleeping for %d seconds...."%(sleep_time))
        time.sleep(sleep_time)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
