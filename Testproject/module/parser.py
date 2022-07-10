import requests
import sys
from datatypes import Recipe, Ingredient
import ZapankaParser

if len(sys.argv) < 2:
        print("needs an URL to work")
        exit(-1)
url = str(sys.argv[1]);

pageContents = requests.get(url)
recipe = ZapankaParser.ParseHtmlPage(pageContents)

print(recipe.getName())
print(recipe.getServingsize())
for e in recipe.getAllIngredientDescriptions():
        print(e)