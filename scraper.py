import requests
from bs4 import BeautifulSoup

#input url (step 2)
URL = input("Paste Allerhande link:")
#scrape information from allerhande
# URL = 'https://www.ah.nl/allerhande/recept/R-R1195268/spitskoolsalade-met-wortel-en-augurk'
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')

#find all ingredients + units
units = soup.find_all('p',{"class":"recipe-ingredients-list_unit__12elq"})
ingredienten = soup.find_all('p',{'class':'recipe-ingredients-list_name__ZFxE7'})

#initialisation for csv file writing
filename = "ingredienten.csv"
f = open(filename,"w")

headers = "units, ingredient\n"

f.write(headers)

#loop through units list
list_unit = []
for u in units :
    ingredient_unit = u.text
    list_unit.append(ingredient_unit)

#loop through ingredients list
list_name = []
for i in ingredienten :
    ingredient_name = i.text
    list_name.append(ingredient_name)

#combine two lists and write them to csv file
index = 0
list_all = []
for a in list_unit :
    list_all.append(list_unit[index])
    list_all.append(list_name[index])
    f.write(list_unit[index] + "," + list_name[index] + "\n")
    index = index + 1

f.close()
