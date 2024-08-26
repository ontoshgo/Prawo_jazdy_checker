from selenium import webdriver
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
import os

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--headless=new")

driver: WebDriver = webdriver.Chrome(options=chrome_options)
driver.get("https://info-car.pl/new/prawo-jazdy/sprawdz-status-prawa-jazdy")

WebDriverWait(driver, 10).until(expected_conditions.element_to_be_clickable((By.ID, "cookiescript_close"))).click()

search_wait = WebDriverWait(driver, 60).until(
    expected_conditions.visibility_of_element_located((By.ID, "searchType"))
)
searchType = driver.find_element(By.ID, "searchType")
searchType.send_keys("PESEL", Keys.ENTER)

input_fields = driver.find_elements(By.CSS_SELECTOR, ".input-flex input")
# 1 search type
# 2 pesel
# 3 name
# 4 surname

pesel = input_fields[1]
name = input_fields[2]
surname = input_fields[3]
checkbox = driver.find_element(By.ID, "regulations")

#Just set the this as environmental values
pesel.send_keys(os.environ["PESEL"])
name.send_keys(os.environ["NAME"])
surname.send_keys(os.environ["SURNAME"])

ActionChains(driver).move_to_element(checkbox).click().perform()

send_button = driver.find_element(By.CSS_SELECTOR, ".submit-box button")

ActionChains(driver).move_to_element(send_button).click().perform()

WebDriverWait(driver,60).until(
    expected_conditions.presence_of_element_located((By.CSS_SELECTOR, ".status-text span"))
)
status = driver.find_element(By.CSS_SELECTOR, ".status-text span").text

print(status)

print("\n")
isMoving = status != "Wprowadzone dane są nieprawidłowe, nieaktualne (dokument został już wydany) lub nie zostały jeszcze wprowadzone do bazy danych. Sprawdź uważnie wszystkie dane, ewentualnie popraw i spróbuj jeszcze raz."

print(isMoving)

driver.quit()
