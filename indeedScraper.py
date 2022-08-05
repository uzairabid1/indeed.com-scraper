import csv
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException

search = ['Contour Software']                   
url = "https://pk.indeed.com/companies?from=gnav-homepage"
browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
browser.get(url)
browser.implicitly_wait(10)
data = []
reviews = []
review_header = ["company","rating",'review_rating', 'overall_review',
                     'job','current/former','location','date','pros','cons','work/balance','compensation/benefits','job security','management','culture', 'review_description', 'review_url']  

def getDetailedReviews():
    for x in range(0,21):
         co = str(x)
         company_xp = '//div[@itemprop="name"]'
         company_name = browser.find_element(By.XPATH,company_xp).text
         total_rating_xp = "//span[@class='css-1vlfpkl e1wnkr790']"
         company_rating_xp = browser.find_element(By.XPATH,total_rating_xp).text[0:3]
         xp = "div[data-testid='reviewsList']>div:nth-child(" + str(x) + ")"
         try:
            xp_rating = xp+">div>div:nth-child(1)>div>button"
            rating = browser.find_element(By.CSS_SELECTOR, xp_rating).text
         except NoSuchElementException:            
            rating= ""
            continue
         try:
            xp_overall = xp + ">div>div:nth-child(2)>h2>a"
            overall = browser.find_element(By.CSS_SELECTOR, xp_overall).text
         except NoSuchElementException:            
            overall = ""
            continue
         try:
            xp_overall = xp + ">div>div:nth-child(2)>h2>a"
            url = browser.find_element(
                By.CSS_SELECTOR, xp_overall).get_attribute("href")
         except NoSuchElementException:           
            url = ""
            continue
         try:
            xp_job_title_date_city = xp + ">div>div:nth-child(2)>div:nth-child(2)>span"
            j_d_c = browser.find_element( By.CSS_SELECTOR, xp_job_title_date_city).text.strip().replace('\n', '') 
            current_former = j_d_c[j_d_c.find("(")+1:j_d_c.find(")")]
            x = j_d_c.split("-")
            if len(x) > 3:
                job = x[1].strip().partition('(')[0]  
                location = x[2].strip()
                date = x[3].strip()
            else:    
           
             job = x[0].strip().partition('(')[0]
             location = x[1].strip() 
             date = x[2].strip()
            
         except NoSuchElementException:       
            job = ""
            location = ""
            date = ""
            current_former = ""

         try:
            
            xp_pros = "(//h2[contains(.,'Pros')]/following-sibling::div)[%s]" %(co) 
            pros = browser.find_element(By.XPATH,xp_pros).text.strip()
         except NoSuchElementException:
            pros = ""
            

         try:
            xp_cons = "(//h2[contains(.,'Cons')]/following-sibling::div)[%s]" %(co)
            cons = browser.find_element(By.XPATH,xp_cons).text.strip()
         except NoSuchElementException:
            cons = "" 
            

         try:
            xp_work_bal = "//div[contains(text(),'out of 5 stars for Work/Life Balance')]"
            xp_compen = "//div[contains(text(),'out of 5 stars for Compensation/Benefits')]"
            xp_job_security = "//div[contains(text(),'out of 5 stars for Job Security/Advancement')]"
            xp_management = "//div[contains(text(),'out of 5 stars for Management')]" 
            xp_culture = "//div[contains(text(),'out of 5 stars for Culture')]"
            work_bal = browser.find_element(By.XPATH,xp_work_bal).text.replace('out of 5 stars for Work/Life Balance','').strip()
            compensation = browser.find_element(By.XPATH,xp_compen).text.replace('out of 5 stars for Compensation/Benefits','').strip()
            job_s = browser.find_element(By.XPATH,xp_job_security).text.replace('out of 5 stars for Job Security/Advancement','').strip()
            management = browser.find_element(By.XPATH,xp_management).text.replace('out of 5 stars for Management','').strip()
            culture = browser.find_element(By.XPATH,xp_culture).text.replace('out of 5 stars for Culture','').strip()

         except NoSuchElementException:
            work_bal=""
            compensation=""
            job_s=""
            management = ""
            culture = ""
            

         try:
            xp_description = xp + ">div>div:nth-child(2)>div[data-tn-component='reviewDescription']"
            description = browser.find_element(
                By.CSS_SELECTOR, xp_description).text.strip().replace('\n','')
         except NoSuchElementException:     
            continue

         row = [company_name,company_rating_xp,rating, overall, job,current_former,location,date,pros,cons,work_bal,compensation,job_s,management,culture,description, url]
         reviews.append(row)     
            
def getCsv(data, filename, header):
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(data) 


def main():
   
    i = 0  
    for company in search: 
         flag = True         
         company = company.replace(' ', '+')
         browser.get("https://pk.indeed.com/companies/search?q="+company)
         reviews_link = browser.find_element(By.XPATH, "//div[@class='css-u2negz eu4oa1w0']//div[1]//div[2]//ul[1]//li[1]/a") 
         reviews_url = reviews_link.get_attribute('href')  

         while(flag==True):
            browser.get(reviews_url+'?fcountry=ALL&start='+str(i))               
            next_page_link = browser.find_elements(By.XPATH,"//a[@data-tn-element='next-page']")
            print(len(next_page_link))
            getDetailedReviews()
            if len(next_page_link)>0:
              i+=20
              flag = True
            else:
             flag = False       
           
 
    getCsv(reviews,'reviews.csv',review_header)
    browser.close()


main()
