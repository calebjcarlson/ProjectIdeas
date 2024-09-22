import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

class MySpider(scrapy.Spider):
    name = "selenium_spider"  # Name of your spider

    # Set the path to the Chromedriver
    DRIVER_PATH = 'chromedriver-win64\\chromedriver.exe'

    # The URL you want to scrape
    start_urls = ['https://onlineradiobox.com/us/northcoastsgreatesthits/playlist/?cs=us.wwl870am1053fm']

    def __init__(self, *args, **kwargs):
        super(MySpider, self).__init__(*args, **kwargs)

        # Set up Chrome options (use --headless if you want it to run in the background)
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Optional, remove if you want to see the browser
        chrome_options.add_argument("--ignore-certificate-errors")

        # Create a service object for ChromeDriver
        webdriver_service = Service(self.DRIVER_PATH)

        # Use Selenium to manage the ChromeDriver version automatically
        self.driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)

    def parse(self, response):
        # Use Selenium to load the page and extract data
        self.driver.get(response.url)
        
        # Extract elements using Selenium
        names = self.driver.find_elements(By.CLASS_NAME, "track_history_item")
        
        # Loop through the extracted names and yield them as Scrapy items
        tracks = [name.text for name in names]

        # Save the scraped text to a file
        with open('playlist.txt', 'w', encoding='utf-8') as file:
            for track in tracks:
                file.write(f"{track}\n")

        # Close the Selenium browser
        self.driver.quit()
        
        # Yield results for Scrapy to handle
        for track in tracks:
            yield {'track': track}
