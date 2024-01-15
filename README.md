# Outbound Links Automation
# Track-Outbound-Links
Use this automation code to find all the outbound links in a webpage, it will check the domain with the base url before tracking the outbound link.

## Overview

This Python script automates the process of finding valid outbound links from a list of base URLs provided in a CSV file. The script uses Selenium to interact with a web browser, checks whether each outbound link belongs to the same domain as the base URL, and saves the results to another CSV file.

## Prerequisites

- Python 3.x
- Selenium (`pip install selenium`)
- Webdriver (e.g., chromedriver for Chrome) - Make sure it is in your system PATH or provide the path explicitly in the script.
- 

## Usage
Install dependencies:
-pip install selenium
-pip install webdriver_manager

Prepare the input CSV file:
- Create a CSV file named urls.csv in the same folder as the script.
- Add base URLs to track outbound links.
- Run the script: "python find_outbound_links.py"

Configuration
- You can customize the script by adjusting the parameters such as the webdriver choice, timeout settings, and CSV file names directly in the script.

Notes
- Ensure that you have the appropriate webdriver executable installed (e.g., chromedriver for Chrome) and it is in your system PATH or provide the path explicitly in the script.
- The script includes error handling for common exceptions during web scraping, making it robust in dealing with various situations.

License
- This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgements
- Special thanks to the developers of Selenium for providing a powerful web automation library.
- Feel free to contribute and report issues!
