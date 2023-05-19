# Python program to demonstrate
# Webdriver For Firefox
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

input_street_name = input("Enter the target street name: ")
# input_street_name = "鄉事會坊"
# input_street_name = "大埔"

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
    buttons = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, f"{className}"))
    )

    try:
        for button in buttons:
            button.click()
    except:
        # Clicking the button
        buttons.click()


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
    table_element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, tableID))
    )

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
enterTextBoxByID("street_name", input_street_name)
clickButtonByID("searchStreetAddress")

while True:
    try:
        time.sleep(0.5)
        clickButtonByTitle("顯示更多")
        # time.sleep(2)
    except:
        break

string_list = scrapeTable("searchStreetAddressList", "tr", "td")

# Split each string into a list of values using '\n' as the separator
split_list = [item.split("\n") for item in string_list]

# Create a DataFrame from the split list
df_streetName = pd.DataFrame(split_list)

# Drop the 1st column with '詳細'
df_streetName.drop(columns=df_streetName.columns[0], axis=1, inplace=True)

# Rename the column headers
df_streetName.columns = ["English Address", "Chinese Address"]

# Add new column which is concantenation of Eng and Chi
df_streetName["街道地址"] = (
    df_streetName["English Address"] + " " + df_streetName["Chinese Address"]
)

# Initialize an empty DataFrame with column names
df_target = pd.DataFrame()
columns = ["街道地址", "位置", "命令狀態", "命令編號", "地址", "日期", "命令類別", "屋宇署檔案編號"]
df_target = pd.DataFrame(columns=columns)

# For each street name, click inside and extract info
for street_itr in range(len(df_streetName["English Address"])):
    print(df_streetName["English Address"][street_itr])

    while True:
        try:
            clickButtonByCSS(f'a.btn.addressSearch[data-addressen="{df_streetName["English Address"][street_itr]}"]')
            break
        except:
            clickButtonByTitle("顯示更多")

    # To expand content by clicking the Arrow
    time.sleep(0.5)
    arrow_IDs = [
        "individualCompiled-s28",
        "individualOutstanding-s28",
        "individualCompiled-s24",
        "commonCompiled-s28",
        "commonOutstanding-s28",
        "individualOutstanding-s24",
    ]
    for id in arrow_IDs:
        try:
            # This button will not wait, unlike the clickButtonByID
            # Find the button element by ID
            button = driver.find_element(By.ID, id)

            # Click the button
            button.click()
        except:
            continue

    # clickButtonByClass('expandBtn.collapsed')
    while True:
        try:
            # This button will not wait, unlike the clickButtonByID
            # Find the button element by CLASS_NAME
            button = driver.find_element(By.CLASS_NAME, "expandBtn.collapsed")

            # Click the button
            button.click()
        except:
            break
    time.sleep(0.5)
    # Find the table's div element by its ID
    # table_div = driver.find_element(By.ID, 'individualOutstanding-s24-content')
    table_IDs = [
        "individualCompiled-s28-content",
        "individualOutstanding-s28-content",
        "commonCompiled-s28-content",
        "commonOutstanding-s28-content",
        "individualOutstanding-s24-content",
        "individualCompiled-s24-content",
    ]
    for id in table_IDs:
        try:
            # This button will not wait, unlike the clickButtonByID
            # Find the button element by ID
            table_div = driver.find_element(By.ID, id)

            # Get all the strings within the div element
            table_strings = table_div.text.splitlines()

            if table_strings == []:
                continue
            else:
                if "individual" in id:
                    indiv_or_buildings = "個別單位"
                else:
                    indiv_or_buildings = "樓宇公用部份"

            for i in range(len(table_strings)):
                if table_strings[i] == "命令編號":
                    val4 = table_strings[i + 1]
                    val3 = table_strings[i + 2]
                elif table_strings[i] == "地址":
                    val5 = table_strings[i + 1]
                elif table_strings[i] == "通知日期":
                    val6 = table_strings[i + 1]
                elif table_strings[i] == "命令類別":
                    val7 = table_strings[i + 1]
                elif table_strings[i] == "屋宇署檔案編號":
                    val8 = table_strings[i + 1]
                    # Append records to the DataFrame using append method
                    record = {
                        "街道地址": f"{df_streetName['街道地址'][street_itr]}",
                        "位置": f"{indiv_or_buildings}",
                        "命令狀態": f"{val3}",
                        "命令編號": f"{val4}",
                        "地址": f"{val5}",
                        "日期": f"{val6}",
                        "命令類別": f"{val7}",
                        "屋宇署檔案編號": f"{val8}",
                    }
                    df_target.loc[len(df_target)] = record

            # print(record)
        except:
            continue

    # # Get all the strings within the div element
    # table_strings = table_div.text.splitlines()

    # for i in range(len(table_strings)):
    #     if table_strings[i] == '命令編號':
    #         val4 = table_strings[i+1]
    #         val3 = table_strings[i+2]
    #     elif table_strings[i] == '地址':
    #         val5 = table_strings[i+1]
    #     elif table_strings[i] == '通知日期':
    #         val6 = table_strings[i+1]
    #     elif table_strings[i] == '命令類別':
    #         val7 = table_strings[i+1]
    #     elif table_strings[i] == '屋宇署檔案編號':
    #         val8 = table_strings[i+1]

    # # Append records to the DataFrame using append method
    # record = {"街道地址": df_streetName['English Address'][0], "位置": "個別單位", "命令狀態": f"{val3}","命令編號": f"{val4}", "地址": f"{val5}", "日期": f"{val6}", "命令類別": f"{val7}", "屋宇署檔案編號": f"{val8}"}
    # df_target.loc[len(df_target)] = record

    # print(df_target)

    clickButtonByID("backToSearch")
    enterTextBoxByID("street_name", input_street_name)
    clickButtonByID("searchStreetAddress")

# Write DataFrame to Excel file with sheet name
df_target.to_excel("Extract.xlsx", sheet_name="extract", index=False)
