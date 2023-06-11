from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def access_site(driver):
    url = "https://search.sunbiz.org/Inquiry/CorporationSearch/ByName"
    driver.get(url)

def navigate_website(driver):
    #Navigate to the website by providing input in the search input
    #Click search and match the first result
    sub_details = []
    company = "sun inc."
    try:
        search_term_xpath = "//div[contains(@class, 'editor-field')]//input[contains(@id, 'SearchTerm')]"
        search_term = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, search_term_xpath)))
        search_term.send_keys(company)

        search_button_xpath = "//div//input[contains(@type, 'submit')]"
        search_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, search_button_xpath)))
        search_button.click()

    except:
        print("error navigating to website")

    try: 
        search_result_xpath = "//div[contains(@id, 'maincontent')]//div[contains(@id, 'search-results')]//table//tbody//tr"
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, search_result_xpath)))
        results = driver.find_elements(By.XPATH, search_result_xpath)

        first_result = results[0].text

        if company in first_result:
            print("No match found")
        
        results[1].find_element(By.XPATH, '//tr//td//a').click()

    except:
        print("Unable to get the search result")

    try:
        company_details_xpath = "//div[contains(@class, 'searchResultDetail')]//div[contains(@class, 'detailSection')]"
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, company_details_xpath)))

        company_details = driver.find_elements(By.XPATH, company_details_xpath)
        
        str_to_check = 'Officer/Director Detail'
        officer_director_details = ''

        for section_detail in company_details:
            if str_to_check in section_detail.text:
                officer_director_details = section_detail
                break

        if officer_director_details:
            details = [detail for detail in officer_director_details.text.split('\n') if detail]
            sub_details = [details[n:n+4] for n in range(2, len(details)-2, 4)]
            
    except:
        print("Could not get the company details")

    driver.quit()
    return sub_details


def main():
    driver = webdriver.Chrome()
    access_site(driver)
    sub_details = navigate_website(driver)
     
    #write the data to csv file
    with open('./results.txt', 'w') as fileWriter:
        fileWriter.write("Title,Name,Address\n")
        for details in sub_details:
            fileWriter.write(f"{details[0].replace('Title', '').strip()},\"{details[1]}\",\"{details[2]} {details[3]}\"\n")






if __name__ == '__main__':
    main()