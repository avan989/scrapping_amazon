#
# COSC 880 - Project - Web scrapping amazon top 100 ebook.
#
# Based on https://www.datacamp.com/community/tutorials/amazon-web-scraping-using-beautifulsoup
# and https://towardsdatascience.com/top-5-beautiful-soup-functions-7bfe5a693482
# Web crawl amazon top ebook

#import
import pandas as pd
import nltk
import requests, re, time, csv
from bs4 import BeautifulSoup 
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize 
nltk.download("stopwords")
nltk.download('punkt')

# https://www.amazon.com/Best-Sellers-Kindle-Store-eBooks/zgbs/digital-text/154606011
# top 100 ebook: https://www.amazon.com/Best-Sellers-Kindle-Store/zgbs/digital-text/ref=zg_bs_pg_1?_encoding=UTF8&pg=1

urls = [
    # "https://www.amazon.com/Best-Sellers-Kindle-Store-Salad-Cooking/zgbs/digital-text/156276011/ref=zg_bs_pg_1?_encoding=UTF8&pg=",
    # "https://www.amazon.com/Best-Sellers-Kindle-Store-Vegan-Cooking/zgbs/digital-text/14530437011/ref=zg_bs_pg_1?_encoding=UTF8&pg=",
    # "https://www.amazon.com/Best-Sellers-Kindle-Store-Vegetable-Cooking/zgbs/digital-text/156277011/ref=zg_bs_pg_1?_encoding=UTF8&pg=",
    # "https://www.amazon.com/Best-Sellers-Kindle-Store-Tablesetting-Cooking/zgbs/digital-text/156273011/ref=zg_bs_pg_1?_encoding=UTF8&pg=",
    # "https://www.amazon.com/Best-Sellers-Kindle-Store-Seasonal-Cooking/zgbs/digital-text/156272011/ref=zg_bs_pg_1?_encoding=UTF8&pg=",
    # "https://www.amazon.com/Best-Sellers-Kindle-Store-Party-Planning-Cooking/zgbs/digital-text/156271011/ref=zg_bs_pg_1?_encoding=UTF8&pg=",
    # "https://www.amazon.com/Best-Sellers-Kindle-Store-Holiday-Cooking/zgbs/digital-text/156270011/ref=zg_bs_pg_1?_encoding=UTF8&pg=",
    # "https://www.amazon.com/Best-Sellers-Kindle-Store-Gourmet-Cooking/zgbs/digital-text/156269011/ref=zg_bs_pg_1?_encoding=UTF8&pg=",
    # "https://www.amazon.com/Best-Sellers-Kindle-Store-Christmas-Hanukkah-Cooking/zgbs/digital-text/156267011/ref=zg_bs_pg_1?_encoding=UTF8&pg=",
    # "https://www.amazon.com/Best-Sellers-Kindle-Store-Brunch-Tea-Cooking/zgbs/digital-text/156266011/ref=zg_bs_pg_1?_encoding=UTF8&pg=",
    # "https://www.amazon.com/Best-Sellers-Kindle-Store-Paleo-Cookbooks/zgbs/digital-text/15280092011/ref=zg_bs_pg_1?_encoding=UTF8&pg=",
    # "https://www.amazon.com/Best-Sellers-Kindle-Store-Low-Salt-Cooking/zgbs/digital-text/156264011/ref=zg_bs_pg_1?_encoding=UTF8&pg=",
    # "https://www.amazon.com/Best-Sellers-Kindle-Store-Low-Fat-Cooking/zgbs/digital-text/156263011/ref=zg_bs_pg_1?_encoding=UTF8&pg=",
    # "https://www.amazon.com/Best-Sellers-Kindle-Store-Low-Cholesterol-Cooking/zgbs/digital-text/156262011/ref=zg_bs_pg_1?_encoding=UTF8&pg=",
    # "https://www.amazon.com/Best-Sellers-Kindle-Store-Low-Carb-Cooking/zgbs/digital-text/6361588011/ref=zg_bs_pg_1?_encoding=UTF8&pg=",
    # "https://www.amazon.com/Best-Sellers-Kindle-Store-Kosher-Cooking/zgbs/digital-text/156261011/ref=zg_bs_pg_1?_encoding=UTF8&pg=",
    # "https://www.amazon.com/Best-Sellers-Kindle-Store-Ketogenic-Cookbooks/zgbs/digital-text/15280091011/ref=zg_bs_pg_1?_encoding=UTF8&pg=",
    # "https://www.amazon.com/Best-Sellers-Kindle-Store-Heart-Healthy-Cooking/zgbs/digital-text/6361587011/ref=zg_bs_pg_1?_encoding=UTF8&pg=",
    # "https://www.amazon.com/Best-Sellers-Kindle-Store-Gluten-Free-Cooking/zgbs/digital-text/6361586011/ref=zg_bs_pg_1?_encoding=UTF8&pg=",
    # "https://www.amazon.com/Best-Sellers-Kindle-Store-Food-Allergy-Cooking/zgbs/digital-text/6361585011/ref=zg_bs_pg_1?_encoding=UTF8&pg=",
    # "https://www.amazon.com/Best-Sellers-Kindle-Store-Diabetic-Sugar-Free-Cooking/zgbs/digital-text/156259011/ref=zg_bs_pg_1?_encoding=UTF8&pg=",
    # "https://www.amazon.com/Best-Sellers-Kindle-Store-Cooking-Kids/zgbs/digital-text/11650855011/ref=zg_bs_pg_1?_encoding=UTF8&pg=",
    # "https://www.amazon.com/Best-Sellers-Kindle-Store-Baby-Food/zgbs/digital-text/6361584011/ref=zg_bs_pg_1?_encoding=UTF8&pg="
    #"https://www.amazon.com/Best-Sellers-Kindle-Store-Paleo-Cookbooks/zgbs/digital-text/15280092011/ref=zg_bs_pg_1?_encoding=UTF8&pg=",
    #"https://www.amazon.com/Best-Sellers-Kindle-Store-Low-Salt-Cooking/zgbs/digital-text/156264011/ref=zg_bs_pg_1?_encoding=UTF8&pg=",
    #"https://www.amazon.com/Best-Sellers-Kindle-Store-Low-Fat-Cooking/zgbs/digital-text/156263011/ref=zg_bs_pg_1?_encoding=UTF8&pg=",
    #"https://www.amazon.com/Best-Sellers-Kindle-Store-Low-Cholesterol-Cooking/zgbs/digital-text/156262011/ref=zg_bs_pg_1?_encoding=UTF8&pg=",
    #"https://www.amazon.com/Best-Sellers-Kindle-Store-Low-Carb-Cooking/zgbs/digital-text/6361588011/ref=zg_bs_pg_1?_encoding=UTF8&pg=",
    #"https://www.amazon.com/Best-Sellers-Kindle-Store-Kosher-Cooking/zgbs/digital-text/156261011/ref=zg_bs_pg_1?_encoding=UTF8&pg=",
    #"https://www.amazon.com/Best-Sellers-Kindle-Store-Ketogenic-Cookbooks/zgbs/digital-text/15280091011/ref=zg_bs_pg_1?_encoding=UTF8&pg=",
    #"https://www.amazon.com/Best-Sellers-Kindle-Store-Heart-Healthy-Cooking/zgbs/digital-text/6361587011/ref=zg_bs_pg_1?_encoding=UTF8&pg=",
    #"https://www.amazon.com/Best-Sellers-Kindle-Store-Healthy-Cooking/zgbs/digital-text/156260011/ref=zg_bs_pg_1?_encoding=UTF8&pg=",
    #"https://www.amazon.com/Best-Sellers-Kindle-Store-Gluten-Free-Cooking/zgbs/digital-text/6361586011/ref=zg_bs_pg_1?_encoding=UTF8&pg=",
    #"https://www.amazon.com/Best-Sellers-Kindle-Store-Food-Allergy-Cooking/zgbs/digital-text/6361585011/ref=zg_bs_pg_1?_encoding=UTF8&pg=",
    #"https://www.amazon.com/Best-Sellers-Kindle-Store-Diabetic-Sugar-Free-Cooking/zgbs/digital-text/156259011/ref=zg_bs_pg_1?_encoding=UTF8&pg=",
    #"https://www.amazon.com/Best-Sellers-Kindle-Store-Cooking-Kids/zgbs/digital-text/11650855011/ref=zg_bs_pg_1?_encoding=UTF8&pg=",
    #"https://www.amazon.com/Best-Sellers-Kindle-Store-Baby-Food/zgbs/digital-text/6361584011/ref=zg_bs_pg_1?_encoding=UTF8&pg="
    "https://www.amazon.com/Best-Sellers-Kindle-Store-Special-Cooking-Appliances/zgbs/digital-text/156257011/ref=zg_bs_pg_1?_encoding=UTF8&pg=",
    "https://www.amazon.com/Best-Sellers-Kindle-Store-American-West-Cooking/zgbs/digital-text/156256011/ref=zg_bs_pg_1?_encoding=UTF8&pg=",
    "https://www.amazon.com/Best-Sellers-Kindle-Store-American-Southwest-Cooking/zgbs/digital-text/156255011/ref=zg_bs_pg_1?_encoding=UTF8&pg=",
    "https://www.amazon.com/Best-Sellers-Kindle-Store-American-South-Cooking/zgbs/digital-text/156254011/ref=zg_bs_pg_1?_encoding=UTF8&pg=",
    "https://www.amazon.com/Best-Sellers-Kindle-Store-American-Soul-Food-Cooking/zgbs/digital-text/156253011/ref=zg_bs_pg_1?_encoding=UTF8&pg=",
    "https://www.amazon.com/Best-Sellers-Kindle-Store-American-Northwest-Cooking/zgbs/digital-text/156252011/ref=zg_bs_pg_1?_encoding=UTF8&pg=",
    "https://www.amazon.com/Best-Sellers-Kindle-Store-New-England-Cooking/zgbs/digital-text/156251011/ref=zg_bs_pg_1?_encoding=UTF8&pg=",
    "https://www.amazon.com/Best-Sellers-Kindle-Store-American-Midwest-Cooking/zgbs/digital-text/156250011/ref=zg_bs_pg_1?_encoding=UTF8&pg=",
    "https://www.amazon.com/Best-Sellers-Kindle-Store-Middle-Atlantic-Cooking/zgbs/digital-text/156249011/ref=zg_bs_pg_1?_encoding=UTF8&pg=",
    "https://www.amazon.com/Best-Sellers-Kindle-Store-California-Cooking/zgbs/digital-text/156247011/ref=zg_bs_pg_1?_encoding=UTF8&pg=",
    "https://www.amazon.com/Best-Sellers-Kindle-Store-Cajun-Creole-Cooking/zgbs/digital-text/156246011/ref=zg_bs_pg_1?_encoding=UTF8&pg=",
    "https://www.amazon.com/Best-Sellers-Kindle-Store-African-American-Cooking/zgbs/digital-text/156244011/ref=zg_bs_pg_1?_encoding=UTF8&pg=",
    "https://www.amazon.com/Best-Sellers-Kindle-Store-Cooking-Food-Wine-Reference/zgbs/digital-text/156206011/ref=zg_bs_pg_1?_encoding=UTF8&pg=",
    "https://www.amazon.com/Best-Sellers-Kindle-Store-Microwave-Cookery/zgbs/digital-text/156205011/ref=zg_bs_pg_1?_encoding=UTF8&pg=",
    "https://www.amazon.com/Best-Sellers-Kindle-Store-Cooking-Kids/zgbs/digital-text/11650854011/ref=zg_bs_pg_1?_encoding=UTF8&pg=",
    "https://www.amazon.com/Best-Sellers-Kindle-Store-Cooking-One/zgbs/digital-text/156203011/ref=zg_bs_pg_1?_encoding=UTF8&pg="

]
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363"}

###########################################################################################################
# 1) 
# Get top 100 name from urls 
# iterate through url and check if there is pagnation. If there is iterate through each pagnation. 
# only 2 since it is the top 100 - 50 per pages - main program for first iteration 
#
###########################################################################################################
def iterate_through_amazon(urls):

    total_product_info = []
    for url in urls:
        for i in range(1,3):
            website_url = url + str(i)
            print(website_url)
            products_info = website_list_view(website_url)
            
            total_product_info += products_info
    

    # wrtie file from data  
    with open('total_product_info_3.csv', mode='w') as product_info:
        
        writer = csv.writer(product_info, delimiter=',')
        
        for row in total_product_info:
            writer.writerow(row)

# get individual product information data from individual product page
def get_website_data(website_url):
   
    try:
        response = requests.get(website_url, headers=headers)
    except requests.exceptions.ConnectionError:
        time.sleep(10) # if connection error, sleep and try again
        
        try: 
            response = requests.get(website_url, headers=headers)
        except requests.exceptions.ConnectionError:
            print("Error connection to %s" %(website_url))
    
    
    amazon_soup = BeautifulSoup(response.content, features='lxml')
    
    if amazon_soup.find(id='productTitle') is not None:

        product_title = amazon_soup.find(id='productTitle').get_text().strip()
        sales_rank_info = amazon_soup.find(id='SalesRank').get_text().strip()
        sales_rank_info_strip_comma = sales_rank_info.replace(',', '')
        sales_rank_list = re.findall('\d+', sales_rank_info_strip_comma ) # https://stackoverflow.com/questions/26825729/extract-number-from-string-in-python, answer from Irshad Bhat
        overall_sales_rank = int(sales_rank_list[0])
     
        return_data = [product_title, overall_sales_rank]
    else: 
        return_data = ["None", "None"]
    
    return return_data;


# iterate through each product_listing and get link to the product page
def website_list_view(website_url):

    final_product_scrap = []
    
    response = requests.get(website_url, headers=headers)
    amazon_soup = BeautifulSoup(response.content, features='lxml')
    
    # get individual product and construct url
    product_list = amazon_soup.select('li.zg-item-immersion span.a-list-item span.aok-inline-block.zg-item a.a-link-normal')  
    amazon_url = ['https://amazon.com' + link['href'] for link in product_list]
    
    # remove duplicate
    url_list = list(set(amazon_url))
    
    # iterate though to get ebook
    for index, url in enumerate(url_list):
    
        if url.find('product-reviews') >= 0:          
            continue
            
        respond = get_website_data(url);
        final_product_scrap.append(respond)  
        
        time_to_pause = 1 * index % 5 
        time.sleep(time_to_pause)
        
        
    return final_product_scrap

            
################################################################################################
# 2) 
# after we get initial excel from top 100, we want to find their competition and their ranking. 
################################################################################################            
def get_keyword_competition_data():
    
    # open files that contain keywords
    keywords = get_csv()
    
    #iterate through title for amazon search engine 
    for text in keywords:
        search_url = "https://www.amazon.com/s?k=" + text + "&i=digital-text&ref=nb_sb_noss_1"
        response = requests.get(search_url, headers=headers)
        amazon_soup = BeautifulSoup(response.content, features='lxml')
        
        total_search_results = amazon_soup.find_all("div", attrs={"class": "sg-col-inner"})

        total_span_tag = total_search_results[0].find_all("span")
        total_search_query = re.findall('\d+', total_span_tag[0].get_text())
        total_search_result_final = int(total_search_query[-1]) 
        print(total_search_result_final)              
               
            

        
        break


#clean up dataset        
def get_csv():
    
    return_data = []
    file_name = "total_product_info.csv"
    
    data = pd.read_csv(file_name, sep=',', header=None)
    data[0] = data[0].replace(r'[~`!@#$%^&*()_+-={[}}|\:;"\'<,>.?/]', '', regex=True)
    
    # code from https://www.geeksforgeeks.org/removing-stop-words-nltk-python/
    stop_words = set(stopwords.words('english')) 
    
    for sentence in data[0]:
        new_sentence = ''
        word_tokens = word_tokenize(sentence) 
          
        filtered_sentence = [w for w in word_tokens if not w in stop_words] 
          
        filtered_sentence = [] 
          
        for w in word_tokens: 
            if w not in stop_words: 
                filtered_sentence.append(w) 
      
        for index, word in enumerate(filtered_sentence):
        
            if index == 10:
                break
                
            new_sentence += word + " "

        return_data.append(new_sentence)
    
    return return_data       

if __name__ == '__main__':
    
    # Gets top 100 data
    iterate_through_amazon(urls)
    
    # Iterate through the top 100 data saved in the files to get ranking informations
    # get_keyword_competition_data()
    
    
    print("finish")