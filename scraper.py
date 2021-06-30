import requests
import json
import random
from bs4 import BeautifulSoup

URL = input("Paste Allerhande link:")
# URL = 'https://www.ah.nl/allerhande/recept/R-R1193949/kofte-met-yoghurtsaus' #hard-coded url for testing

#import from this website: https://www.dietdoctor.com/recipes/the-keto-bread

page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')

#find title, servings, units, ingredients, steps, rating and nutritional values
title_soup = soup.find('h1',{"class":"recipe-header_title__2no_y"})
servings_soup = soup.find('p',{"class":"recipe-ingredients_count__297va"})
units = soup.find_all('p',{"class":"recipe-ingredients-list_unit__12elq"})
ingredienten = soup.find_all('p',{'class':'recipe-ingredients-list_name__ZFxE7'})
steps = soup.find_all('div',{'class':'recipe-steps_step__3wRuI'})
rating_soup = soup.find_all('svg',{'class':'allerhande-icon svg svg--svg_star-filled'})
nutrition_name_soup = soup.find_all('div',{'class':'recipe-footer-nutrition_nutrition__1bfDg'})

#calculate rating by counting "filled stars"
rating = len(rating_soup)

#extract title from soup
title = title_soup.text

#extract servings from soup, split to only get number
servings_split = servings_soup.text.split()
servings = servings_split[0]

#replace fractions
# 1/2 \u00BD - 0.5      ½
# 1/4 \u00BC - 0.25     ¼
# 3/4 \u00BE - 0.75     ¾
# 1/3 \u2153 - 0.33     ⅓
# 1/8 \u215B - 0.125    ⅛
# 2/3 \u2154 - 0.66     ⅔
# 1/5 \u2155 - 0.2      ⅕

# steps = steps_soup.replace('\u00BD', '0.5')

#loop through units list to add amounts and units to their corresponding lists
list_unit = []
list_amount = []
unit_index = 0
for u in units :
    ingredient_unit = u.text
    split = ingredient_unit.split()

    if len(split) == 2 :
        list_amount.append(split[0])
        list_unit.append(split[1])
    else:
        list_amount.append(split[0])
        list_unit.append("")        

#fix weird fractions, it looks for fractions, converts them to decimals,
#then if it is a number and a fraction, it adds them together(7½ becomes 7,5)
#and it makes sure that everything is a float in the list.
list_amount_fixed = []
for r in list_amount :
    if '½' in r :
        h = r.replace('½', ' 0.5')
        split = h.split()
        if len(split) > 1:
            added = float(split[0]) + float(split[1])
            list_amount_fixed.append(float(added))
        else :
            list_amount_fixed.append(float(split[0]))
    elif '¼' in r :
        q = r.replace('¼', ' 0.25')
        split = h.split()
        if len(split) > 1:
            added = float(split[0]) + float(split[1])
            list_amount_fixed.append(float(added))
        else :
            list_amount_fixed.append(float(split[0]))
    elif '¾' in r :
        tq = r.replace('¾', ' 0.75')
        split = h.split()
        if len(split) > 1:
            added = float(split[0]) + float(split[1])
            list_amount_fixed.append(float(added))
        else :
            list_amount_fixed.append(float(split[0]))
    else :
        list_amount_fixed.append(float(r))
    # oe = r.replace('⅛', ' 0.125')
    # list_amount_fixed.append(oe)
    # ot = r.replace('⅓', ' 0.33')
    # list_amount_fixed.append(ot)
    # tt = r.replace('⅔', ' 0.66')
    # list_amount_fixed.append(tt)
    # of = r.replace('⅕', ' 0.2')
    # list_amount_fixed.append(of)

# print(type(list_amount_fixed[0]))
# print(type(list_amount_fixed[5]))


# splittemp = list_amount_fixed[13].split()
# print(splittemp)
# if len(splittemp) > 1 :
#     added = float(splittemp[0]) + float(splittemp[1])
    # print(added)


#loop through ingredients list to add ingredients to it's list
list_name = []
for i in ingredienten :
    ingredient_name = i.text
    list_name.append(ingredient_name)

#extract steps and add them together as one long string
description = ''
for s in steps :
    step = s.p.text
    # print('----' + step)
    description += step

#find all nutrition values on website, check if title matches, then grab the value of the nutrition value and store it
for n in nutrition_name_soup :
    if n.span.text == 'energie':
        calories = n.find('span',{'class':'recipe-footer-nutrition_nutritionValue__EhKyZ'}).text
    elif n.span.text == 'koolhydraten':
        carbs = n.find('span',{'class':'recipe-footer-nutrition_nutritionValue__EhKyZ'}).text
    elif n.span.text == 'vet':
        fats = n.find('span',{'class':'recipe-footer-nutrition_nutritionValue__EhKyZ'}).text
    elif n.span.text == 'eiwit':
        protein = n.find('span',{'class':'recipe-footer-nutrition_nutritionValue__EhKyZ'}).text

#generate random ID
recipe_id = random.randint(0,9999)

#generating the JSON
#loop through all recipe ingredients, extract all information (name, amount and unit), append it to all_ingredients list
all_ingredients = []
recipe_index = 0
for r in list_name :
    recipe_ingredient = {'name':list_name[recipe_index],
                        'amount':list_amount_fixed[recipe_index],
                        'unit':list_unit[recipe_index]}  #add , and ]
    recipe_index += 1
    # print(recipe_ingredient)


    all_ingredients.append(recipe_ingredient)

#add the rest of the information to the JSON file
recipe = {
    'title': title,
    'servings': float(servings),
    'description': description,
    'recipe-ingredients': [all_ingredients],
    'favourite':True,
    'rating':rating,
    'nutritionValuesPerServing':[{
        'carbs': float(carbs),
        'fats': float(fats),
        'protein': float(protein),
        'calories': float(calories)
    }] ,
    'id': recipe_id   
}

#dump information into JSON file
with open('recipe.json','w') as recipe_dumped :
    json.dump(recipe, recipe_dumped)

print('Scraping done and JSON file created!')


# recipe = {
#   'title': 'string',
#   'description':'string',
#   'servings':'int'
#   'ingredients':[
#       {
#       "name":"string"
#       "amount":"int"
#       "unit":"string"
#       },
#       {
#       "name":"string"
#       "amount":"int"
#       "unit":"string"
#       }
#   ],
#   'steps':[
#       'string','string'
#       ]
# }

# breuken omzetten: 
# from fractions import Fraction

# test1 = Fraction(1)
# test2 = Fraction(1, 4)
# test3 = Fraction(0.5)


# print(test1)
# print(test2)
# print(test3)

# print(test2*2)