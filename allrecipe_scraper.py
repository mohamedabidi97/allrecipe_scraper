# Import packages
from selenium import webdriver
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import requests
import time as t 
from csv import writer
# Create  a DataFrame
df = pd.DataFrame(columns=['Name' , 'Type' , 'Cooking Time', 'Preration Time', 'Servings','Ingredients', 'Steps' , 'Full nutrition' , 'Image']) 
categories_names  = []
categories_href  = []
links_of_recipe = []
URL = 'https://www.allrecipes.com/recipes/'
req = requests.get(URL)
soup = BeautifulSoup(req.content, 'html.parser') 
# categories Names : 
container = soup.find('div', class_ = 'col-container').findAll("a")
for cato in container : 
    categories_names.append(cato.get_text())
# categories href : 
container = soup.find('div', class_ = 'col-container').findAll("a")
for cato in container : 
    categories_href.append(cato.get('href'))
print('length of categories name  :  '+ str(len(categories_names)))
print('length of categories href  :  '+ str(len(categories_href)))
for href,name in zip(categories_href,categories_names ): 
    print('*************** Href of categorie ********************')
    print(href)
    print('\n')
    print('************* All pages *******************')
    print('\n')
    for i in range(1,6) :
            links_all_recipes = []
            URL = href+'?sort=Title&page='+str(i)
            print(URL)
            req = requests.get(URL)
            soup = BeautifulSoup(req.content, 'html.parser')
            table_links = soup.findAll('div' ,class_ = 'grid-card-image-container')
            for link in table_links : 
                link = link.find('a') 
            # links contain the link of each recipe page 
                links_all_recipes.append(link.get('href'))
            print('\n')
            print('******************** length of all recipes **********************')
            print('\n')
            for link in links_all_recipes :
                print(len(links_all_recipes))
                print('****************** Link of recipe ******************' )
                print('\n')
                print(link)
                print('\n')
                req = requests.get(link)
                soup = BeautifulSoup(req.content, 'html.parser')
                print('\n')
                print('********** name of recipe ********** \n')
                try:
                    name_recipe = soup.find("h1", class_= 'headline heading-content').text
                    print(name_recipe)
                    print('\n')
                except : 
                    name_recipe ='NA'
                
                print('********** times ********** \n')
                try :
                    time = soup.find_all('div' ,class_ = 'recipe-meta-item-body')
                    prep_time = ''
                    cook_time= ''
                    if len(time) > 2 : 
                        prep_time = time[0].get_text().strip()
                        cook_time =  time[1].get_text().strip()
                    print(prep_time +' '+ cook_time)
                    print('\n')
                except : 
                    prep_time : 'NA'
                    cook_time :'NA'

                print('********** Servings ********** \n')
                try  :
                    soup = BeautifulSoup(req.content, 'html.parser')
                    servings = ''
                    servi = soup.find('div', class_='recipe-adjust-servings__original-serving')
                    if servi : 
                        servings = servi.text.strip() 
                        print(servi.text.strip())
                except :
                    servings = 'NA'


                print('********** Ingredients  ********** \n')
                try : 
                    ing= soup.find_all('span' , class_="ingredients-item-name")
                    ings = [] 
                    if ing is not None :
                        for i in ing : 
                            ings.append(i.get_text().strip())
                            print(i.get_text().strip())
                        ings.append(ings)
                    print('\n')
                except : 
                    ings = ['NA']
                print('********** Cooking steps  ********** \n')
                try : 
                    for i in soup.find_all('div', class_ = 'paragraph') :
                        steps = []
                        if i is not None :
                            steps.append(i.get_text().strip())
                            print(i.get_text().strip())
                    print('\n')
                except : 
                    steps = ['NA']

                print('********** Full Nutrition ********** \n')
                try :
                    nutrition = soup.find('div' ,class_ = 'nutrition-body')
                    nut= []
                    if nutrition is not None : 
                        nutri = nutrition.get_text().strip().replace('\n','').replace(' ','').replace('%','%  ').replace('g','g ')
                        nut.append(nutri)  
                        print(nutri)
                        print('\n')
                except : 
                    nutrition = ['NA']

                print('********** Image of recipe ********* \n')
                try : 
                    img = soup.find('div', class_='image-container').find('img').get('src')
                    if img is not None :
                        print(img)
                    print('\n')
                except : 
                    img = 'NA'
            
                df = df.append({'Name' : name_recipe  , 'Type': name , 'Cooking Time' : cook_time, 'Preration Time' : prep_time, 'Servings' : servings,'Ingredients' : ings, 'Steps' : steps , 'Full nutrition' : nut, 'Image' :img},ignore_index=True)
                print(df.shape)
# save the data into csv file
df.to_csv('data.csv', index=False, encoding='utf-8')
      

    











