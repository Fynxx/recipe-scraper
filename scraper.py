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
        print(calories)
    elif n.span.text == 'koolhydraten':
        carbs = n.find('span',{'class':'recipe-footer-nutrition_nutritionValue__EhKyZ'}).text
        print(carbs)
    elif n.span.text == 'vet':
        fats = n.find('span',{'class':'recipe-footer-nutrition_nutritionValue__EhKyZ'}).text
        print(fats)
    elif n.span.text == 'eiwit':
        protein = n.find('span',{'class':'recipe-footer-nutrition_nutritionValue__EhKyZ'}).text
        print(protein)

#generate random ID
recipe_id = random.randint(0,9999)
print(recipe_id)

#generating the JSON
#loop through all recipe ingredients, extract all information (name, amount and unit), append it to all_ingredients list
all_ingredients = []
recipe_index = 0
for r in list_name :
    recipe_ingredient = {'name':list_name[recipe_index],
                        'amount':list_amount[recipe_index],
                        'unit':list_unit[recipe_index]}  #add , and ]
    recipe_index += 1
    # print(recipe_ingredient)


    all_ingredients.append(recipe_ingredient)

#add the rest of the information to the JSON file
recipe = {
    'title': title,
    'servings': servings,
    'description': description,
    'recipe-ingredients': [all_ingredients],
    'favourite':True,
    'rating':rating,
    'nutritionValuesPerServing':[{
        'carbs': carbs,
        'fats': fats,
        'protein': protein,
        'calories': calories
    }] ,
    'id': recipe_id   
}

#dump information into JSON file
with open('recipe'+str(recipe_id)+'.json','w') as recipe_dumped :
    json.dump(recipe, recipe_dumped)


# {
#     "name": "Italian keto meatballs with mozzarella cheese",
#     "servings": 4,
#     "description": "Tomato sauce, rich and comforting. Mozzarella, fresh and creamy. Meatballs, with just the right touch of onion and basil. It's like spaghetti night, without the carbs. Enjoy every ketolicious bite!",
#     "recipe-ingredients":{

#     }
#     "instructions": "1. Place ground beef, parmesan cheese, egg, salt and spices in a bowl and blend thoroughly. Form the mixture into meatballs, about 1 oz (30 grams) each. It helps to keep your hands wet while forming the balls.\r\n2. Heat up the olive oil in a large skillet and sauté the meatballs until they're golden brown on all sides.\r\n3. Lower the heat and add the canned tomatoes. Let simmer for 15 minutes, stirring every couple of minutes. Season with salt and pepper to taste. Add parsley and stir. You can prepare the dish up to this point for freezing.\r\n4. Melt the butter in a separate frying pan and fry the spinach for 1-2 minutes, stirring continuously. Season with salt and pepper to taste. Add the spinach to the meatballs, and stir to combine.\r\n5. Serve with mozzarella cheese on top, torn into bite-sized pieces.\r\n",
#     "favorite": true,
#     "rating": 3,
#     "nutritionValuesPerServing": {
#         "netCarbs": 0.0,
#         "carbs": 0.0,
#         "fats": 0.0,
#         "protein": 0.0,
#         "calories": 200.0
#     },
#     "id": 1
# }

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