# Web Scraping Notes

The GasBuddy website was selected due to providing a webpage for retrieving price data for the selected city.  See below for notes on web scraping script.

- Web scraping is required due to no usable information can be found in the page source that would be retrieved from a simple HTTP GET request.  A browser must be used to allow the JavaScript code to run and render the webpage.  

- The data for each station is located within a visual card.  These cards can be located and iterated over to extract data from each station.

- A dropdown control is provided to toggle between different fuel types.  The script can interact with this item to cause the cards to reload for each fuel type of interest.

- No efforts have been made to validate the pricing data from the website.  As the goals of the overall project were to demonstrate the use of web scraping to aid analytics, it was assumed that this source data is accurate.

- Modules within the src directory are described below.
    - `scrape.py` - This is the script which uses the [Selenium WebDriver](https://www.selenium.dev/documentation/webdriver/) to control a headless Chrome browser.  The script running on a scheduled as implemented using the Windows Task Scheduler.
    
    - `gmail_util.py` - This short script provides the ability to send an email to indicate the status of a scraping attempt.  Extracted data being dumped as JSON for a successful attempt or error information in the case of an exception.  This being an optional component to the overall data acquisition process.