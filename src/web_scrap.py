from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

def scrape_faqs(url, output_file):
    # Setup Selenium WebDriver
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Load the webpage
    driver.get(url)
    time.sleep(5)  # Wait for the page to fully load

    # Get page source and parse it with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()  # Close the browser

    # Step 1: Extract the main content section
    main_content = soup.find("div", class_="col-12 col-lg-9 docs-content")
    
    if not main_content:
        print("Error: Could not find the main FAQ section!")
        return
    
    # Step 2: Extract all question-answer pairs
    faq_items = main_content.find_all("div", class_="accordion-item")
    
    with open(output_file, "w", encoding="utf-8") as file:
        for item in faq_items:
            # Extract question
            question_element = item.find("p", class_="mb-0 me-2")
            if question_element:
                question = question_element.text.strip()
                file.write(f"Question: {question}\n")
            
            # Extract answer
            answer_element = item.find("div", class_="text-stone p-4")
            if answer_element:
                answer = answer_element.get_text(separator="\n", strip=True)
                file.write(f"Answer: {answer}\n")
            
            file.write("\n")  # Add a separator between FAQ items

    print(f"FAQs saved to {output_file}")

# URL of the FAQ page
faq_url = "https://www.contentstack.com/docs/faqs#contentstack-datasync-faqs"
output_filename = "ans.txt"

scrape_faqs(faq_url, output_filename)
