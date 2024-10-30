## Actividad: Cobertura de pruebas

La cobertura de pruebas es el porcentaje de líneas de código que se ejecutan durante todas las pruebas. 
Una alta cobertura de pruebas te da confianza de que una gran cantidad de código fue ejecutada durante las pruebas.
A su vez, mientras más líneas de código se ejecuten a través de pruebas, más confiado puedes estar de que el código funciona como se espera.

La actividad consta en ir agregando casos de prueba para mejorar la cobertura leyendo las lineas de codigo faltante.

## Paso 1:
En una primera instancia solo tenemos de 2 pruebas.

La primera prueba verifica que solo se haya creado una cuenta. Se hace uso del modelo AAA.
```python
def test_create_an_account(self):
        #arange
        data = ACCOUNT_DATA[0]       #Configura los datos
        #act
        account = Account(**data)         #Se crea una instancia de account incluyendo sus datos para luego guardarlos
        account.create()
        #assert
        assert len(Account.all()) == 1       #Se verifica que solo se haya creado una sola cuenta
```

Para la segunda prueba se verifica la creacion de multiples cuentas. Tambien se hace uso del modelo AAA.

```python
    def test_create_all_accounts(self):
        #Arange
        for data in ACCOUNT_DATA:       #El for permite el uso de todos los datos de ACCOUNT_DATA
        #Act
            account = Account(**data)      #Se crea y se guarda todas las cuentas de la base de datos
            account.create()
        #Assert
        assert len(Account.all()) == len(ACCOUNT_DATA)    #Verificamos con len() si la cantidad de cuentas creadas son las mismas que estas en ACCOUNT_DATA
```

Hacemos pasar las pruebas con la siguiente comanda :

```
pytest --cov=./
```
Este es el resultado a la ejecución de ambas pruebas:

![image](https://github.com/user-attachments/assets/5b549ec2-2e88-4875-8404-15c028d4f169)


## Paso 2 
Agregamos mas pruebas para cubrir mas lineas de código, en esta caso el siguiente método a probar es:

```python
def __repr__(self):
    return '<Account %r>' % self.name
```

La prueba:
```python
def test_repr(self):
    # Arrange 
    account = Account()  # Crear una instancia de la cuenta y establece un nombre "Manuel"
    account.name = "Manuel" 
    # Act 
    result = str(account)  # Obtiene la representación en cadena de la cuenta
    # Assert 
    assert result == "<Account 'Manuel'>"  # Verifica que el resultado sea "Manuel"
```

Ejecutamos la comanda:
```
pytest --cov=./
```
Resultado:

![image](https://github.com/user-attachments/assets/071fc5f5-5694-4a71-be24-0d732d7cc33c)


Seguimos agregando mas pruebas, el metodo a probar es:

```python
def to_dict(self) -> dict:
    """Serializa la clase como un diccionario"""
    return {c.name: getattr(self, c.name) for c in self.__table__.columns}
```

La prueba:

```python
def test_to_dict():
    # Arrange
    random_key = random.randint(0, len(ACCOUNT_DATA) - 1)# usa import random
    data = ACCOUNT_DATA[random_key]
    account = Account(**data)
        
    # Act
    account.create()
    result = account.to_dict()

    # Assert
    # Verificar que los campos del diccionario coinciden con los atributos de la instanci
    assert account.name == result["name"], f"Nombre esperado: {account.name}, obtenido: {result['name']}"
    assert account.email == result["email"], f"Email esperado: {account.email}, obtenido: {result['email']}"
    assert account.phone_number == result["phone_number"], f"Número de teléfono esperado: {account.phone_number}, obtenido: {result['phone_number']}"
    assert account.disabled == result["disabled"], f"Estado 'disabled' esperado: {account.disabled}, obtenido: {result['disabled']}"
        
    # Verificar que 'date_joined' está presente y es una cadena en formato ISO
    assert "date_joined" in result, "'date_joined' no está presente en el diccionario resultante"
        
    # Verificar el formato de 'date_joined'
    try:
       datetime.datetime.fromisoformat(str(result["date_joined"]))
    except ValueError:
       assert False, f"'date_joined' no está en formato ISO: {result['date_joined']}"
```

Pasamos los test y vemos el progreso:

![image](https://github.com/user-attachments/assets/3ad443ea-6719-496b-87da-653496ccc883)





