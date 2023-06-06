from datetime import datetime as time
from persistence.generate_account_number import GenerateAccount

class Storage:
    __accounts = {}
    def __init__(self, name = None, document = None, balance = None, type_account = None, password = None) -> None:
        self.__name = name
        self.__document = document
        self.__balance = balance
        self.__data_created = str(time.now())
        self.__type = type_account
        self.__password = password 
        self.__number_acount = GenerateAccount().account 
        if (name != None and document != None and balance != None and type_account != None and password != None):
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
        
        withdrawal = float(input('Digite el valor a retirar: '))
        withdrawal = withdrawal if withdrawal > 0 else 0
        
        if withdrawal == 0:
            print('Esa transacción no es válida')
            return None
        
        if ( data['balance'] >= withdrawal ):
            data['balance'] -= withdrawal
        elif(((data['balance']+data['coupe']) >= withdrawal) and (data['type_account'] == 'corriente')):
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
            
            
    def authentication(self, data, password_try) -> bool:
        if data == None:
            print('No existe dicho registro')
            return False
        password = data.get('password')
        if password != password_try:
            print('Contraseña incorrecta')
            return False
        return True