#from calendar import c
import requests
from bs4 import BeautifulSoup
class Ingredient:
        def __init__(self, name, amount=None, unit=None, note=None):
                self.name = name
                self.amount = amount
                self.unit = unit
                self.note = note

        def __str__(self):
                result = self.name
                if self.amount and self.unit:
                        result = f'{result} - {self.amount}{self.unit}' 
                if self.note:
                        result = f'{result} - {self.note}'  
                return result 
                #if not self.note:
                #        return f'{self.name} - {self.amount}{self.unit}'
                #else:
                #        return f'{self.name} - {self.amount}{self.unit} - {self.note}'   

                                #for ingredient_amount in ingredient.find('span', {'class': 'wprm-recipe-ingredient-amount'}):
                                #        print(ingredient_amount.text)
                                #for ingredient_unit in ingredient.find('span', {'class': 'wprm-recipe-ingredient-unit'}):
                                #        print(ingredient_unit.text)
                                #ingredient_name in ingredient.find('span', {'class': 'wprm-recipe-ingredient-name'}):
                                #        print(ingredient_name.text)


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
                        ingredient_note = litag.find('span', {'class': 'wprm-recipe-ingredient-notes'})
                        for ingredient in litag.find_all('span', {'class': 'wprm-recipe-ingredient-unit-system-1'}):
                                ingredient_amount = ingredient.find('span', {'class': 'wprm-recipe-ingredient-amount'})
                                ingredient_unit = ingredient.find('span', {'class': 'wprm-recipe-ingredient-unit'})
                        if not ingredient_name:
                                print("damaged Item !")
                                continue;
                        if not ingredient_amount and not ingredient_unit and not ingredient_note:
                                allIngredients.append( Ingredient(ingredient_name.text))
                        if ingredient_amount and not ingredient_unit and not ingredient_note:
                                allIngredients.append( Ingredient(ingredient_name.text,  ingredient_amount.text))
                        if ingredient_amount and ingredient_unit and ingredient_note:
                                allIngredients.append( Ingredient(ingredient_name.text, ingredient_amount.text, ingredient_unit.text, ingredient_note.text))
                        if ingredient_amount and ingredient_unit and not ingredient_note:
                                allIngredients.append( Ingredient(ingredient_name.text, ingredient_amount.text, ingredient_unit.text))
print("Finshed parsing")
for e in allIngredients:
        print(e)

        #print(divtag.text)
        #for ultag in soup.find_all('ul', {'class': 'wprm-recipe-ingredient-group'}):
        #        for litag in ultag.find_all('li'):
        #                print(litag.text)