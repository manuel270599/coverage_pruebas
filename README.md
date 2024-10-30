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
