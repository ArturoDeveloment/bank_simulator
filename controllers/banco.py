from persistence.accounts import Storage

class logic_banc:
    def __init__(self):
        self.bank = Storage()
        
    def create_acount(self):
        cuenta = input("\n1. Para cuenta de ahorros\n2. Para cuenta corriente\nIngrese: ")
        cuenta = "ahorros" if cuenta == "1" else "corriente" if cuenta == "2" else None
        try:
            data = {
                "name": input("Ingrese su nombre: "),
                "document": abs(int(input("Ingrese su documento: "))),
                "balance": float(input("Ingrese el saldo inicial: ")),
                "type_account": cuenta,
                "password": input("Ingrese contraseña: ")
            }
        except Exception as e:
            print(f"Error de entrada de datos -> {e}")

        if data.get('type_account') == None:
            print('Tipo de cuenta incorrecto')
            return None

        data['balance'] = data.get('balance') if data.get('balance') >= 0 else 0
        new_person = Storage(**data)
    
    def show_account(self):
        account = int(input("Ingrese su número de cuenta: "))
        password = input("Digite su contraseña: ")
        self.bank.show_account(account, password)
    
    def make_transaction(self):
        account = int(input("Ingrese su número de cuenta: "))
        password = input("Digite su contraseña: ")
        self.bank.make_transaction(account, password)