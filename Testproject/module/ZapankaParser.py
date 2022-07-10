from bs4 import BeautifulSoup
from bs4 import Tag as HtmlTag
import requests
from datatypes import Recipe, Ingredient

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

def ParseHtmlPage(page: requests.Response) -> Recipe:

    soup = BeautifulSoup(page.content, "html.parser")
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
                            
    return Recipe(recipeName,recipeServingsInfo,ingredients)