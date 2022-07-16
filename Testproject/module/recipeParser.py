from abc import ABC, abstractmethod
from datatypes import Recipe

class RecipeParser(ABC):
    @abstractmethod
    def parse_html_page(page: bytes) -> Recipe:
        pass