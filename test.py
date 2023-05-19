# Python program to demonstrate
# Webdriver For Firefox
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Firefox()
driver.get(
    "https://www.bd.gov.hk/tc/resources/online-tools/orders-search/ordersearch.html"
)


def clickButtonByTitle(title):
    # Finding the button by its title attribute
    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, f"[title={title}]"))
    )

    # Clicking the button
    button.click()


def clickButtonByID(id):
    # Finding the button by its title attribute
    button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, id)))

    # Clicking the button
    button.click()


def clickButtonByCSS(cssString):
    # Find the <a> element by its class attribute
    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, cssString))
    )

    # Clicking the button
    button.click()


def clickButtonByClass(className):
    # Find the <a> element by its class attribute
    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, f"{className}"))
    )

    # Clicking the button
    button.click()


def enterTextBoxByID(id, text):
    # Finding the textbox by its ID
    textbox = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, id))
    )

    # Clearing the existing text (if any)
    textbox.clear()

    # Typing text into the textbox
    textbox.send_keys(text)


def scrapeTable(tableID, tr, td):
    string_list = []
    # Find the table element by its ID
    table_element = driver.find_element(By.ID, tableID)

    # Get all the elements within the table
    table_rows = table_element.find_elements(By.TAG_NAME, "tr")

    # Iterate over the rows and print the text content of each cell
    for row in table_rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        row_data = [cell.text for cell in cells]
        if len(row_data) > 0:
            string_list.append(row_data[0])

    return string_list


clickButtonByTitle("接受")
clickButtonByTitle("街道名稱")
enterTextBoxByID("street_name", "Tai Po")
clickButtonByID("searchStreetAddress")

string_list = scrapeTable("searchStreetAddressList", "tr", "td")

# Split each string into a list of values using '\n' as the separator
split_list = [item.split("\n") for item in string_list]

# Create a DataFrame from the split list
df = pd.DataFrame(split_list)

# Drop the 1st column with '詳細'
df.drop(columns=df.columns[0], axis=1, inplace=True)

# Rename the column headers
df.columns = ["English Address", "Chinese Address"]


# while True:
#     try:
#         clickButtonByTitle("顯示更多")
#         time.sleep(2)
#     except:
#         break

# ----------------------------------------------------------

# # Finding all the buttons
# table = driver.find_elements(By.ID, "searchStreetAddressList")

# # Find all the tr elements within the table
# tr_elements = table.find_elements(By.TAG_NAME, "tr")

# # Scrape the content of each td element within each tr element
# for tr in tr_elements:
#     td_elements = tr.find_elements(By.TAG_NAME, "td")
#     for td in td_elements:
#         content = td.text
#         print(content)  # Replace with your desired processing or storage logic


# # Clicking each button to open a new tab
# for button in buttons:
#     # Click the button to open a new tab
#     button.click()

#     # Switch to the new tab
#     driver.switch_to.window(driver.window_handles[-1])

#     # Perform any further actions in the new tab
#     time.sleep(2)
#     # Close the new tab
#     driver.close()

#     # Switch back to the main tab
#     driver.switch_to.window(driver.window_handles[0])

#     # Add a delay between each button click
#     time.sleep(2)  # Replace with the desired delay in seconds

# # Finding the button with the name "詳細"
# button = WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), '詳細')]"))
# )

# # Clicking the button
# button.click()

# clickButtonByID("btn arrow addressSearch")

# # Find the table element
# table = driver.find_element(By.XPATH, "//table")

# # Find all the tr elements within the table
# tr_elements = table.find_elements(By.TAG_NAME, "tr")

# # Scrape the content of each td element within each tr element
# for tr in tr_elements:
#     td_elements = tr.find_elements(By.TAG_NAME, "td")
#     for td in td_elements:
#         content = td.text
#         print(content)  # Replace with your desired processing or storage logic
