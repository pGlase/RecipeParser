from dataclasses import dataclass

@dataclass
class Ingredient:
        name:str
        unit:str
        quantity:str
        note:str

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

@dataclass
class Recipe:
        name:str
        servingsInfo:str
        ingredients:list[Ingredient]


        def getName(self) -> str:
                return self.name

        def getServingsize(self) -> str:
                return self.servingsInfo

        def getAllIngredientDescriptions(self) -> str:
                return list(map(lambda x:x.getDescription(), self.ingredients))
