from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

# Initialize the Edge webdriver
driver = webdriver.Edge()

def scrape_nces_data():
    # Navigate to the URL
    driver.get("https://nces.ed.gov/ccd/schoolsearch/")
    driver.maximize_window()

    # Locate the School Name search box and type "A"
    school_name_input = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//input[@name='InstName']")))
    school_name_input.send_keys("A")

    # Click the search button
    search_button = driver.find_element(By.XPATH, "(//input[@type='submit'])[2]")
    search_button.click()

    # Wait until results are displayed
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//td[@valign='middle']//strong//font[@color='#FFFFFF']"))
    )

    # Extracting school data
    school_rows = driver.find_elements(By.XPATH, "//table/tbody/tr/td/table")

    data = []
    for row in school_rows:
        # Check for presence of serial number, indicating it's a valid school row
        serial_numbers = row.find_elements(By.XPATH, ".//font[@size='1'][@color='#80BB71']")
        if serial_numbers:
            details = row.find_elements(By.XPATH, ".//td")
            if len(details) > 4:
                # Extracting merged address details
                merged_address = details[1].text.split('\n')
                school_name_details = merged_address[0].strip()
                address = merged_address[1].strip() if len(merged_address) > 1 else ""
                
                phone = details[2].text

                school_data = {
                    "School Name": school_name_details,
                    "Address": address,
                    "Phone": phone
                }
                data.append(school_data)

    return data

def save_to_csv(data):
    if not data:
        return

    keys = data[0].keys()
    with open("C:/Users/91989/Downloads/schools_data.csv", "w", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)

if __name__ == "__main__":
    try:
        scraped_data = scrape_nces_data()
        save_to_csv(scraped_data)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()
