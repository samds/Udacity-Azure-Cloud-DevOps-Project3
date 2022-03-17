# #!/usr/bin/env python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
import datetime
    
def log(text):
    ct = datetime.datetime.now()
    print(f"[{ct}] {text}")

url = 'https://www.saucedemo.com/'
log('Starting the browser...')
driver = webdriver.Chrome()
# --uncomment when running in Azure DevOps.
options = ChromeOptions()
options.add_argument("--headless") 
driver = webdriver.Chrome(options=options)

# Start the browser and login with standard_user
def login(user, password):
    log('Browser started successfully. Navigating to the demo page to login.')
    log('Navigating to ' + url)
    driver.get(url)
    driver.find_element(by=By.CSS_SELECTOR, value="input[id='user-name']").send_keys(user)
    driver.find_element(by=By.CSS_SELECTOR, value="input[id='password']").send_keys(password)
    driver.find_element(by=By.CSS_SELECTOR, value="input[id='login-button']").click()
    assert driver.current_url == (url + 'inventory.html')
    log(f'Logged as {user}.') # never output password!
    log(f'Redirected to {driver.current_url}.')
    return driver

# Add all products to the cart
def add_all_items(driver):
    items = driver.find_elements(by=By.CSS_SELECTOR, value="div[class='inventory_item']")
    for item in items:
        name = item.find_element(by=By.CSS_SELECTOR, value="div[class='inventory_item_name']").text
        log(f'Add item {name}')
        item.find_element(by=By.CLASS_NAME, value="btn_inventory").click()

# Remove all products from the cart
def remove_all_items(driver):
    items = driver.find_elements(by=By.CSS_SELECTOR, value="div[class='cart_item']")
    for item in items:
        name = item.find_element(by=By.CSS_SELECTOR, value="div[class='inventory_item_name']").text
        log(f'Remove item {name}')
        item.find_element(by=By.CLASS_NAME, value="cart_button").click()


driver = login('standard_user', 'secret_sauce')
add_all_items(driver)
driver.find_element(by=By.CSS_SELECTOR, value="#shopping_cart_container > a").click()
log(f'Redirected to {driver.current_url}.')
remove_all_items(driver)