#from calendar import c
import requests
from bs4 import BeautifulSoup
Bs4Tag = BeautifulSoup.element.Tag

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
                result = self.name
                if self.amount and self.unit:
                        result = f'{self.amount} {self.unit} - {result}' 
                elif not self.amount and self.unit:
                        result = f'{result} - {self.unit}'
                elif self.amount and not self.unit:
                        result = f'{self.amount} - {result}'   
                if self.note:
                        result = f'{result} - {self.note}'  
                return result 

#def ZapankaTagToIngredient(name:Bs4Tag, amount:Bs4Tag=None, unit:Bs4Tag=None, note:Bs4Tag=None ) -> Ingredient:
#        return None   


allIngredients = list(())
URL = "https://biancazapatka.com/de/indian-chickpea-curry-vegan-gluten-free/#recipe"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
#ZapankaParser

#Skip to recipe block directly
for countGroup, divtag in enumerate(soup.find_all('div', {'class': 'wprm-recipe-ingredient-group'})):
        print (f'Group #{countGroup}:')
        #every "component" of the dish
        for subGroup, ultag in enumerate(divtag.find_all('ul', {'class': 'wprm-recipe-ingredients'})):
                print (f'       SubGroup #{subGroup}:')
                #one ingredient
                for ingreCount, litag in enumerate(ultag.find_all('li', {'class': 'wprm-recipe-ingredient'})):
                        print (f'               Ingredient #{ingreCount}:')
                        #read only the correct unitsystem
                        ingredient_name = litag.find('span', {'class': 'wprm-recipe-ingredient-name'})
                        print(type(ingredient_name))
                        ingredient_note = litag.find('span', {'class': 'wprm-recipe-ingredient-notes'})
                        for ingredient in litag.find_all('span', {'class': 'wprm-recipe-ingredient-unit-system-1'}):
                                ingredient_amount = ingredient.find('span', {'class': 'wprm-recipe-ingredient-amount'})
                                ingredient_unit = ingredient.find('span', {'class': 'wprm-recipe-ingredient-unit'})
                        if not ingredient_name:
                                print("damaged Item, skipping...")
                                continue;
                        allIngredients.append( Ingredient(ingredient_name, ingredient_amount, ingredient_unit, ingredient_note))
print("Finshed parsing")
for e in allIngredients:
        print(e)

        #print(divtag.text)
        #for ultag in soup.find_all('ul', {'class': 'wprm-recipe-ingredient-group'}):
        #        for litag in ultag.find_all('li'):
        #                print(litag.text)