#from calendar import c
import requests
from bs4 import BeautifulSoup
import sys

class Ingredient:
        def __init__(self, name, amount=None, unit=None, note=None):
                self.name = name.text
                if amount:
                        self.amount = amount.text
                else:
                        self.amount = None
                if unit:
                        self.unit = unit.text
                else:
                        self.unit = None
                if note:
                        self.note = note.text
                else:
                        self.note = None

        def __str__(self):
                result = f'{self.name}' 
                if self.amount and self.unit:
                        result = f'{self.amount} {self.unit} - {self.name}' 
                elif not self.amount and self.unit:
                        result = f'{self.name} - {self.unit}'
                elif self.amount and not self.unit:
                        result = f'{self.amount} - {self.name}'   
                if self.note:
                        result = f'{result} - {self.note}'  
                return result

allIngredients = list(())

if len(sys.argv) < 2:
        print("needs an URL to work")
        exit(-1)
URL = str(sys.argv[1]);

page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")
#ZapankaParser

recipeNameElement = soup.find('h2', {'class': 'wprm-recipe-name'})
print(f'Recipe: {recipeNameElement.text}')

servingsElement = soup.find('span', {'class': 'wprm-recipe-servings-with-unit'})
print(f'Ingredients for {servingsElement.text}')

#Skip to recipe block directly
for divtag in soup.find_all('div', {'class': 'wprm-recipe-ingredient-group'}):
        #every "component" of the dish
        for ultag in divtag.find_all('ul', {'class': 'wprm-recipe-ingredients'}):
                #one ingredient
                for litag in ultag.find_all('li', {'class': 'wprm-recipe-ingredient'}):
                        ingredient_name = litag.find('span', {'class': 'wprm-recipe-ingredient-name'})
                        ingredient_note = litag.find('span', {'class': 'wprm-recipe-ingredient-notes'})

                        #read only the correct unitsystem
                        for ingredient in litag.find_all('span', {'class': 'wprm-recipe-ingredient-unit-system-1'}):
                                ingredient_amount = ingredient.find('span', {'class': 'wprm-recipe-ingredient-amount'})
                                ingredient_unit = ingredient.find('span', {'class': 'wprm-recipe-ingredient-unit'})
                        if not ingredient_name:
                                print("damaged Item, skipping...")
                                continue;
                        allIngredients.append( Ingredient(ingredient_name, ingredient_amount, ingredient_unit, ingredient_note))

for e in allIngredients:
        print(e)