from uuid import uuid4
from random import randint

class GenerateAccount():
    def __init__(self) -> None:
        self.__account = self.__number_account()
        
    def __number_account(self):
        return int(f"{str(uuid4().int)[0:6]}{str(randint(1000, 9999))}")
    
    @property
    def account(self):
        return self.__account

