from dataclasses import dataclass
import requests
from bs4 import BeautifulSoup
from bs4 import Tag as HtmlTag
import sys

@dataclass
class Ingredient:
        name:str
        unit:str
        quantity:str
        note:str

        #@getDescription 
        def getDescription(self) -> str:
                result = ""
                if self.quantity:
                        result = f'{self.quantity} '
                if self.unit:
                        result = f'{result}{self.unit}\t'
                result = f'{result}{self.name}'
                if self.note:
                        result = ''.join(f'{result} - {self.note}')
                return result

def getValueOrEmpty(tag:HtmlTag) -> str:
        if not tag:
                return ''
        else:
                return tag.text

def makeIngredientFromHtmlTags(nameTag:HtmlTag, amountTag:HtmlTag=None, unitTag:HtmlTag=None, noteTag:HtmlTag=None) -> Ingredient:
        amount:str = getValueOrEmpty(amountTag)
        unit:str = getValueOrEmpty(unitTag)
        note:str = getValueOrEmpty(noteTag)
        return Ingredient(nameTag.text, unit, amount, note)

@dataclass
class Recipe:
        name:str
        servingsInfo:str
        ingredients:list[Ingredient]

        #@getName
        def getName(self) -> str:
                return self.name

        #@getServingsize
        def getServingsize(self) -> str:
                return self.servingsInfo

        #@getAllIngredientDescriptions
        def getAllIngredientDescriptions(self) -> str:
                return list(map(lambda x:x.getDescription(), self.ingredients))

if len(sys.argv) < 2:
        print("needs an URL to work")
        exit(-1)
URL = str(sys.argv[1]);

page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")
#ZapankaParser

#Parse metadata
recipeNameElement = soup.find('h2', {'class': 'wprm-recipe-name'})
recipeName = f'Recipe: {recipeNameElement.text}'

servingsElement = soup.find('span', {'class': 'wprm-recipe-servings-with-unit'})
recipeServingsInfo = f'Ingredients for {servingsElement.text}'


ingredients = list(())
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
                                continue

                        ingredients.append(makeIngredientFromHtmlTags(ingredient_name, ingredient_amount, ingredient_unit, ingredient_note))
                        
recipe = Recipe(recipeName,recipeServingsInfo,ingredients)

print("Finished parsing\n")
print(recipe.getName())
print(recipe.getServingsize())
for e in recipe.getAllIngredientDescriptions():
        print(e)