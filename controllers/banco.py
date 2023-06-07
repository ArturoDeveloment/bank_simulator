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
            
            comparison = self.bank.request_id_client(data.get('document'))
            if comparison == 'exists':
                return None
            
        except Exception as e:
            print(f"Error de entrada de datos -> {e}")
            return None

        if data.get('type_account') == None:
            print('Tipo de cuenta incorrecto')
            return None

        data['balance'] = data.get('balance') if data.get('balance') >= 0 else 0
        new_person = Storage(**data)
    
    def show_account(self):
        account = self.get_account()
        password = input("Digite su contraseña: ")
        self.bank.show_account(account, password)
        print('Aditional space')
        self.bank.request_balance(account, password)
    
    def make_transaction(self):
        account = self.get_account()
        password = input("Digite su contraseña: ")
        self.bank.make_transaction(account, password)
    
    def deposit(self):
        account = self.get_account()
        password = input("Digite su contraseña: ")
        self.bank.account_deposit(account, password)
    
    def request_data(self):
        account = self.get_account()
        password = input("Digite su contraseña: ")
        self.bank.request_balance(account, password)
    
    def get_account(self)-> int:
        try:
            account = int(input("Ingrese su número de cuenta: "))
            return account
        except Exception as e:
            print("Error: ", e)
            return -1
    
    def password_forgot(self):
        account = self.get_account()
        if account == -1:
            return None
        document = int(input('Digite su cedula o identificación: '))
        name = input('Digite su nombre: ')
        type_account = input("""
Su tipo de cuenta es: 
    1. ahorros
    2. corriente
opción: """)
        type_account = 'corriente' if type_account == '2' else 'ahorros' if type_account == '1' else None
        self.bank.password_change(account, document, name, type_account)
    
    def iter(self):
        self.bank.iter_accounts_users()