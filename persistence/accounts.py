from datetime import datetime as time
from persistence.generate_account_number import GenerateAccount

class Storage:
    __id_cedulas = []
    __accounts = {}
    def __init__(self, name = None, document = None, balance = None, type_account = None, password = None) -> None:
        self.__name = name
        self.__document = document
        self.__balance = balance
        self.__data_created = str(time.now())
        self.__type = type_account
        self.__password = password 
        self.__number_acount = GenerateAccount().account 
        if (name != None):
            self.__id_cedulas.append(document)
            self.__set_data()
        
    def get_data(self):
        data = {
            "number_acount": self.__number_acount,
            "password": self.__password,
            "name": self.__name,
            "document": self.__document,
            "type_account": self.__type,
            "balance": self.__balance,
            "data_created": self.__data_created,
        }
        if (data.get('type_account') == 'corriente'):
            data['coupe'] = self.__balance * 0.35
            data['debt'] = 0
            print('Se habilita un cupo inicial del 35% sobre el saldo\nApartair de ahora cada ingreso aumenta un cupo de 5% sobre lo ingresado')
        return data

    def __set_data(self):
        self.__accounts[self.__number_acount] = self.get_data()
        print(f'Su número de cuenta Sr {self.__name} es: {self.__number_acount}')
    
    def show_account(self, number_account, password_try):
        data = self.__accounts.get(number_account)
        
        if not(self.authentication(data, password_try)):
            return None
        
        titles = [
            'Número cuenta', 'Contraseña', 'Nombre', 'Documento', 'Tipo de cuenta', 'Saldo', 'Fecha de creación' 
        ]
        if (data.get('type_account') == 'corriente'):
            titles.append('Cupo')
            titles.append('Deuda')
        
        for title, value in zip(titles, data.values()):
            if title == 'Contraseña':
                value = '*' * len(value)
            print(f"{title:<30} -> {value:<30}")

    def make_transaction(self,number_account, password_try):
        data = self.__accounts.get(number_account)
        
        if not(self.authentication(data, password_try)):
            return None
        
        try:
            withdrawal = float(input('Digite el valor a retirar: '))
        except Exception as e:
            print(e)
            return None
        
        withdrawal = withdrawal if withdrawal > 0 else 0
        
        if withdrawal == 0:
            print('Esa transacción es válida')
            return None
        
        if ( data['balance'] >= withdrawal ):
            data['balance'] -= withdrawal
        elif((data['type_account'] == 'corriente') and ((data['balance']+data['coupe']) >= withdrawal)):
            withdrawal -= data['balance']
            data['balance'] = 0
            data['debt'] += withdrawal
            print(f'Su deuda de cupo está en {data["debt"]}')
            data['coupe'] -= withdrawal
        else:
            if( data['balance'] == 0 and data['type_account'] == 'ahorros'):
                print('Su cuenta de ahorros no tiene fondos')
            if( data['balance'] > 0 and data['type_account'] == 'ahorros'):
                print('Usted no tiene esa cantidad de fondos')
            elif(data['balance'] > 0  and data['type_account'] == 'corriente' and data['coupe'] > 0):
                print('Su transacción está fuera de rango')
            elif(data['balance'] == 0  and data['type_account'] == 'corriente' and data['coupe'] == 0):
                print(f'Usted no tiene fondos y debe {data["debt"]}')
            else:
                print('Trasacción fuera de rango')
            return None
        print('Transacción exitosa')

    def account_deposit(self, number_account, password_try):
        data = self.__accounts.get(number_account)
        if not(Storage.authentication(data, password_try)):
            return False
        try:
            to_deposit = float(input('Digite cuánto va a depositar: '))
        except Exception as e:
            print(e)
            return None
        if to_deposit <= 0:
            print('Nose puede completar la transación')
            return None
        # review if user haves debts
        if (data.get('type_account') == 'corriente' and data.get('debt') > 0 ):
            debt_get = data.get('debt')
            if to_deposit > debt_get:
                to_deposit -= debt_get
                data['debt'] = 0
                if (data.get('type_account') == 'corriente'):
                    data['coupe'] += debt_get
                
            elif debt_get >= to_deposit:
                data['debt'] -= to_deposit
                debt_get -= data['debt']
                # if account current save or increase the coupe
                if (data.get('type_account') == 'corriente'):
                    data['coupe'] += debt_get
                print(f"{'Se cubre la deuda y se aumenta el cupo ':^40}")
                return True
            print(f"{'No tiene deuda, recupera cupo y aumenta su saldo':^40}")
            
        data['balance'] += to_deposit
        print(f'Su salario aumento en un {to_deposit}')
        # for ever deposit the coupe increase at 5% it calculate over deposit not balance, something it if account is corriente
        if (data.get('type_account') == 'corriente' and data.get('balance') >= 0):
            increase_coupe = to_deposit * 0.05
            data['coupe'] += increase_coupe
            print(f'Su cupo aumenta en un 5% : {increase_coupe}')
    
    def request_balance(self, number_account, password_try):
        data = self.__accounts.get(number_account)
        if not(Storage.authentication(data, password_try)):
            return False
        presentation = f"Sr(a) {data.get('name')} su saldo actual es: "
        print(f"\n{presentation:*^30}")
        print(f"Su saldo es: {data.get('balance') - data.get('debt')}" if data.get('type_account') == 'corriente' else f"Su saldo es: {data.get('balance')}")
        coupe = data.get('coupe') if data.get('type_account') == 'corriente' else 0
        print(f"Su cupo actual es {data.get('coupe')} ") if (data.get('coupe') != None and data.get('coupe') == 0) else None
        print(f"Su cupo actual es: {coupe}") if coupe != 0 else None
        print(f"El total disponible es: {data.get('balance') + coupe}")
    
    def request_id_client(self, id_user):
        if id_user in self.__id_cedulas:
            print('Ya tiene una cuenta registrada')
            return 'exists'
        return None
    
    def iter_accounts_users(self):
        for account, data in self.__accounts.items():
            cupo = '' if data.get('type_account') == 'ahorros' else f"->|Cupo: ${data.get('coupe')}"
            print(f"{account: <20} -> |name: {data.get('name'): <30} -> |Contraseña: {data.get('password').replace(data.get('password'), '*' * len(data.get('password'))): <30} ->|saldo: ${data.get('balance'): <20}{cupo}")
    
    def password_change(self, number_acount, document, name, type_account):
        data = self.__accounts.get(number_acount)
        if data.get('document') == document and data.get('name') == name and data.get('type_account') == type_account:
            password_new = input('Digite la nueva contraseña: ')
            data['password'] = password_new
            print('Se aplicó el cambio')
            return None
        print('Hay incongruencias en la verificación')
        return None
        
    @staticmethod
    def authentication(data, password_try) -> bool:
        if data == None:
            print('No existe dicho registro')
            return False
        password = data.get('password')
        if password != password_try:
            print('Contraseña incorrecta')
            return False
        return True