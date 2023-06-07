from controllers.banco import logic_banc
from os import system

class MenuPrincipal():
    def __init__(self):
        self.bank = logic_banc()
        while True:
            self.option = self.set_option()
            option = self.select_option()
            if option == 'exit':
                break
    
    def set_option(self)-> int:
        return int(input("""
    1. Crear Cuenta
    2. Ver cuenta
    3. Retirar
    4. Depositar en cuenta
    5. Consultar saldo
    6. Consultar client
    7. Olvide mi contraseña
    8. Salir

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
                self.bank.deposit()
            case 5:
                self.bank.request_data()
            case 6:
                self.bank.iter()
            case 7:
                self.bank.password_forgot()
            case 8:
                return 'exit'
            case _:
                print("option not found")

if __name__ == '__main__':
    MenuPrincipal()