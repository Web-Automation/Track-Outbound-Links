# Use this automation program to find all the outbound links in a webpage.
# This automation code has a domain check function which will first check the domain of the provided base url webpage then it will cross-check all the outbound links that doesn't belong to the same domain.
# You need to provide the path of a CSV file containg "base URLs" in which you need to track the outbound links.
# After successfully execution of this program, a CSV file will generate which contains all the outbound links with the base url from these outbound links have been found.  
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from urllib.parse import urlparse
from selenium import webdriver
import csv


# Function to check if URLs belong to the same domain
def is_same_domain(url1, url2):
    # Extract domain components from the URLs
    domain1 = urlparse(url1).netloc.split('.')[-2:]
    domain2 = urlparse(url2).netloc.split('.')[-2:]
    
    # Compare the domain components to check if they are the same
    return domain1 == domain2

# Set up the webdriver (make sure you have chromedriver or geckodriver installed)
driver = webdriver.Chrome()  # You can use other drivers like Firefox by changing this line

# Read base URLs from CSV file
base_urls = []
with open('urls.csv', 'r') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        base_urls.extend(row)

# List to store valid outbound links
valid_outbound_links = []

for base_url in base_urls:
    # Open the webpage
    driver.get(base_url)

    # Find all elements containing href attribute
    elements_with_href = driver.find_elements(By.XPATH, '//*[@href]')

    # Find all anchor tags
    anchor_tags = driver.find_elements(By.TAG_NAME, 'a')

    # Combine elements containing href and anchor tags
    all_href_elements = elements_with_href + anchor_tags

    # Parse the base URL
    parsed_base_url = urlparse(base_url)

    for element in all_href_elements:
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

# Close the browser window
driver.quit()

# Save valid outbound links to a CSV file
csv_filename = 'valid_outbound_links.csv'
with open(csv_filename, mode='w', newline='') as file:
    fieldnames = ['Base URL', 'Outbound Link']
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()
    for link in valid_outbound_links:
        writer.writerow(link)

print(f"Valid outbound links saved to {csv_filename}")

