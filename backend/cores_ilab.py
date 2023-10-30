# REQUIREMENTS: 
# Install Selenium: pip install selenium
# Copy in the path the chromedriver from https://chromedriver.chromium.org/downloads 
# For the newest chromedriver check https://googlechromelabs.github.io/chrome-for-testing/
# WARNING: The chromedriver version must match the version of the Chrome browser installed on your computer.
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, NoSuchWindowException
from selenium.webdriver.chrome.options import Options


iLab_url = 'https://chop.ilab.agilent.com/landing/101'



def login_iLab(iLab_url=iLab_url):
    # set chrome options
    chrome_options = Options()
    chrome_options.add_experimental_option("excludeSwitches",['enable-automation', 'enable-logging']) 
            # ['enable-automation']  <--  remove "Chrome is being controlled by automated test software"    
            # ['enable-logging'])    <--  USB-triggered error messages are sent to log, not to console; 

    # keep the browser open after the script ends    
    chrome_options.add_experimental_option("detach", True)  
    
    # disable address bar (uncomment the line below after confirming Penn url pattern)
    # chrome_options.add_argument("-app=" + iLab_url)

    # initialize a browser window
    browser = webdriver.Chrome(chrome_options)
    browser.get(iLab_url)

    # Here the user is giveen time (wait_seconds) to enter the user name and password in the browser window
    # When the user is logged in iLab, the "user_dropdown" button becomes visible. 
    #EDITED
    wait_seconds = 3
    try:
        WebDriverWait(browser, wait_seconds).until(EC.visibility_of_element_located((By.ID, "user_dropdown")))
        logged_in = True
    except (TimeoutException, NoSuchElementException) as e:
        # TODO: add code to manage this error
        logged_in = False
    except NoSuchWindowException:
        logged_in = False
        
    chrome_options = Options()

    return browser, logged_in

def get_user_info(browser, logged_in):
    if logged_in:
        # construct the profile URL
        profile_url = browser.current_url + "/about/show_profile"

        browser.get(profile_url)
        # get the name 
        name_label = browser.find_element(By.XPATH, "//label[@for='name']")
        name = name_label.find_element(By.XPATH, "..").text[5:]
        # get the phone
        phone_label = browser.find_element(By.XPATH, "//label[@for='phone']")
        phone = phone_label.find_element(By.XPATH, "..").text[6:]
        # get the email
        email_label = browser.find_element(By.XPATH, "//label[@for='email']")
        email = email_label.find_element(By.XPATH, "..").text[6:]
        # get the labs
        browser.find_element(By.XPATH, "//a[@data-tab='labs']").click()
        expected_cond = EC.visibility_of_element_located((By.XPATH, "//table[@class='ui striped table']"))
        table_element = WebDriverWait(browser, 10).until(expected_cond)
        lab_table_rows = table_element.find_elements(By.XPATH, "./td/a[@class='ui']")
        lab_list = []
        for lab in lab_table_rows:
            lab_list.append(lab.text)
        
    elif not logged_in:
        name = None
        phone = None
        email = None
        lab_list = []
        print( 'Add code for emergency access. (GUI asking the user to enter her/his info)')

    return name, phone, email, lab_list
        
if __name__ ==  '__main__':
    browser, logged_in = login_iLab(iLab_url=iLab_url)
    name, phone, email, lab_list = get_user_info(browser, logged_in)
    print('Name: ', name)
    print('Email: ', email)
    print('Phone: ', phone)
    print('Labs:', lab_list)