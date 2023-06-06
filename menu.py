from controllers.banco import logic_banc
from os import system

class MenuPrincipal():
    def __init__(self):
        self.bank = logic_banc()
        while True:
            self.option = self.set_option()
            self.select_option()
    
    def set_option(self)-> int:
        return int(input("""
    1. Crear Cuenta
    2. Ver cuenta
    3. Retirar
    4. Depositar en cuenta
    5. Consultar saldo
    6. Consultar cliente

Ingrese una opción: """))
    
    def select_option(self):
        match self.option:
            case 1:
                self.bank.create_acount()
            case 2:
                self.bank.show_account()
            case 3:
                self.bank.make_transaction()
            case 4:
                pass
            case 5:
                pass
            case 6:
                pass
            case _:
                print("option not found")