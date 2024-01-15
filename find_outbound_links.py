# Use this automation program to find all the outbound links in a webpage.
# This automation code has a domain check function which will first check the domain of the provided base url webpage then it will cross-check all the outbound links that doesn't belong to the same domain.
# You need to provide the path of a CSV file containg "base URLs" in which you need to track the outbound links.
# After successfully execution of this program, a CSV file will generate which contains all the outbound links with the base url from these outbound links have been found.  
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from urllib.parse import urlparse
from selenium import webdriver
import csv


# This function checks that URLs that're navigating by this program belongs to same domain, it doesn't navigate to other domain which doesn't belong to the parent domain:
# Example URL: "testing.com"(suppose parent domain) then all URLs i.e. test.testing.com, dev.testing.com, uat.testing.com etc..
def is_same_domain(url1, url2):
    # Extract domain components from the URLs
    domain1 = urlparse(url1).netloc.split('.')[-2:]
    domain2 = urlparse(url2).netloc.split('.')[-2:]
    
    # Compare the domain components to check if they are the same
    return domain1 == domain2

# Set up the webdriver:
driver = webdriver.Chrome()  # You can use other drivers like Firefox by changing this line
driver.implicitly_wait(10)  # Set a default timeout for element search

# Read base URLs from CSV file: Replace "urls.csv" file with the CSV file name that contains URLs, put it in the same folder where you have put this code file.
base_urls = []
with open('urls.csv', 'r') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        base_urls.extend(row)

# List to store valid outbound links
valid_outbound_links = []

# Maximum attempts for page load and fetching href links: It avoids the code execution failure if any website takes too long to response 
max_attempts = 3

for base_url in base_urls:
    for attempt in range(max_attempts):
        try:
            # Open the webpage
            driver.get(base_url)

            # Wait for a specific element to be present (adjust as needed)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

            # Find all anchor tags
            anchor_tags = driver.find_elements(By.TAG_NAME, 'a')

            # Parse the base URL
            parsed_base_url = urlparse(base_url)

            for element in anchor_tags:
                for attempt_href in range(max_attempts):
                    try:
                        href = element.get_attribute('href')

                        # Check if the link is not empty
                        if href:
                            # Check if the link is an outbound link (not from the same domain)
                            if not is_same_domain(href, base_url):
                                valid_outbound_links.append({'Base URL': base_url, 'Outbound Link': href})
                                print(f"Valid outbound link from {base_url}: {href}")
                    except StaleElementReferenceException:
                        # Handle StaleElementReferenceException
                        print("StaleElementReferenceException occurred. Skipping this element.")
                    except Exception as e:
                        # Handle other exceptions
                        print(f"An unexpected error occurred for {base_url}: {str(e)}. Attempt {attempt_href + 1}/{max_attempts}. Retrying...")
                        if attempt_href == max_attempts - 1:
                            raise  # Raise the exception if max attempts are reached

            # Break the attempt loop if the page load and href links are successful
            break
        except TimeoutException:
            # Handle TimeoutException
            print(f"TimeoutException occurred for {base_url}. Attempt {attempt + 1}/{max_attempts}. Retrying...")
        except Exception as e:
            # Handle other exceptions
            print(f"An unexpected error occurred for {base_url}: {str(e)}. Attempt {attempt + 1}/{max_attempts}. Retrying...")
            if attempt == max_attempts - 1:
                print("Max attempts reached. Refreshing the browser session...")
                driver.quit()
                driver = webdriver.Chrome()  # Re-initialize the webdriver
            else:
                continue  # Continue with the next attempt

# Close the browser window
driver.quit()

# Save valid outbound links to a CSV file: After the execution of this code a new CSV file will generate that holds all the outbound links, you can change the CSV file name from "valid_outbound_links.csv" to anyone that you like
csv_filename = 'valid_outbound_links.csv'
with open(csv_filename, mode='w', newline='') as file:
    fieldnames = ['Base URL', 'Outbound Link']
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()
    for link in valid_outbound_links:
        writer.writerow(link)

print(f"Valid outbound links saved to {csv_filename}")
