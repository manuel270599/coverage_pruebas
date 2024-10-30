import random
import json
import pytest
import sys
import os
import datetime
from models.account import Account, DataValidationError
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models import db
from models.account import Account


ACCOUNT_DATA = {}

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    """Configura la base de datos antes y después de todas las pruebas"""
    # Se ejecuta antes de todas las pruebas
    db.create_all()
    yield
    # Se ejecuta después de todas las pruebas
    db.session.close()

class TestAccountModel:
    """Modelo de Pruebas de Cuenta"""

    @classmethod
    def setup_class(cls):
        """Conectar y cargar los datos necesarios para las pruebas"""
        global ACCOUNT_DATA
        with open('tests/fixtures/account_data.json') as json_data:
            ACCOUNT_DATA = json.load(json_data)
        print(f"ACCOUNT_DATA cargado: {ACCOUNT_DATA}")

    @classmethod
    def teardown_class(cls):
        """Desconectar de la base de datos"""
        pass  # Agrega cualquier acción de limpieza si es necesario

    def setup_method(self):
        """Truncar las tablas antes de cada prueba"""
        db.session.query(Account).delete()
        db.session.commit()

    def teardown_method(self):
        """Eliminar la sesión después de cada prueba"""
        db.session.remove()

    ######################################################################
    #  C A S O S   D E   P R U E B A
    ######################################################################

    def test_create_an_account(self):
        """Probar la creación de una sola cuenta"""
        data = ACCOUNT_DATA[0]  # obtener la primera cuenta
        account = Account(**data)
        account.create()
        assert len(Account.all()) == 1

    def test_create_all_accounts(self):
        """Probar la creación de múltiples cuentas"""
        for data in ACCOUNT_DATA:
            account = Account(**data)
            account.create()
        assert len(Account.all()) == len(ACCOUNT_DATA)

    def test_repr(self):
        """Prueba la representación de una cuenta"""
        account = Account()
        account.name = "Manuel"
        assert str(account) == "<Account 'Manuel'>"



    def test_to_dict(self):
        """Prueba la conversión de una cuenta a diccionario"""
        # Seleccionar un índice aleatorio válido
        random_key = random.randint(0, len(ACCOUNT_DATA) - 1)# usa import random
        # Obtener los datos de la cuenta seleccionada
        data = ACCOUNT_DATA[random_key]
        # Crear una instancia de Account con los datos seleccionados
        account = Account(**data)
        # Guardar la cuenta en la base de datos
        account.create()
        # Convertir la cuenta a un diccionario
        result = account.to_dict()
        # Verificar que los campos del diccionario coinciden con los atributos de la instanci
        assert account.name == result["name"], f"Nombre esperado: {account.name}, obtenido: {result['name']}"
        assert account.email == result["email"], f"Email esperado: {account.email}, obtenido: {result['email']}"
        assert account.phone_number == result["phone_number"], f"Número de teléfono esperado: {account.phone_number}, obtenido: {result['phone_number']}"
        assert account.disabled == result["disabled"], f"Estado 'disabled' esperado: {account.disabled}, obtenido: {result['disabled']}"
        # Verificar que 'date_joined' está presente y es una cadena en formato ISO
        assert "date_joined" in result, "'date_joined' no está presente en el diccionario resultante"

        try:
           datetime.datetime.fromisoformat(str(result["date_joined"]))
        except ValueError:
            assert False, f"'date_joined' no está en formato ISO: {result['date_joined']}"




    def test_from_dict(self):
        """Prueba establecer atributos de una cuenta desde un diccionario"""
        # Seleccionar un índice aleatorio válido
        random_key = random.randint(0, len(ACCOUNT_DATA) - 1) # usa import random
        # Obtener los datos de la cuenta seleccionada
        data = ACCOUNT_DATA[random_key]
        # Crear una instancia de Account sin establecer atributos
        account = Account()
        # Utilizar el método from_dict() para establecer los atributos desde el diccionario
        account.from_dict(data)
        # Verificar que los atributos de la instancia coinciden con los valores del diccionario
        assert account.name == data["name"], f"Nombre esperado: {data['name']}, obtenido: {account.name}"
        assert account.email == data["email"], f"Email esperado: {data['email']}, obtenido: {account.email}"
        assert account.phone_number == data["phone_number"], f"Número de teléfono esperado: {data['phone_number']}, obtenido: {account.phone_number}"
        assert account.disabled == data["disabled"], f"Estado 'disabled' esperado: {data['disabled']}, obtenido: {account.disabled}"
        # Opcional: Verificar que 'date_joined' no ha sido establecido por from_dict()
        # ya que este campo generalmente se establece automáticamente al crear la cuenta
        assert account.date_joined is None, f"'date_joined' debería ser None, obtenido: {account.date_joined}"

    def test_update_account(self):
        """Prueba la actualización de una cuenta utilizando datos conocidos"""
        # Seleccionar un índice aleatorio válido
        random_key = random.randint(0, len(ACCOUNT_DATA) - 1)
        # Obtener los datos de la cuenta seleccionada
        data = ACCOUNT_DATA[random_key]
        # Crear una instancia de Account con los datos seleccionados
        account = Account(**data)
        # Guardar la cuenta en la base de datos
        account.create()
        # Verificar que la cuenta ha sido asignada un ID
        assert account.id is not None, "La cuenta no fue creada correctamente y no tiene un ID asignado."
        # Modificar uno de los atributos de la cuenta
        original_name = account.name
        account.name = "Rumpelstiltskin"
        # Ejecutar el método update() para guardar los cambios en la base de datos
        account.update()
        # Recuperar la cuenta actualizada desde la base de datos
        found_account = Account.find(account.id)
        # Verificar que el atributo 'name' ha sido actualizado correctamente
        assert found_account.name == account.name, (
                    f"Se esperaba que el nombre fuera '{account.name}', pero se obtuvo '{found_account.name}'."
                )

        # Verificar que otros atributos no han sido alterados
        assert found_account.email == data["email"], (
                    f"El email no debería haber cambiado. Se esperaba '{data['email']}', pero se obtuvo '{found_account.email}'."
                )
        assert found_account.phone_number == data["phone_number"], (
                    f"El número de teléfono no debería haber cambiado. Se esperaba '{data['phone_number']}', pero se obtuvo '{found_account.phone_number}'."
                )
        assert found_account.disabled == data["disabled"], (
                    f"El estado 'disabled' no debería haber cambiado. Se esperaba '{data['disabled']}', pero se obtuvo '{found_account.disabled}'."
                )

    def test_update_invalid_id(self):
        """Prueba la actualización de una cuenta con ID inválido"""
        random_key = random.randint(0, len(ACCOUNT_DATA) - 1)# usa import random
        data = ACCOUNT_DATA[random_key]  
        account = Account(**data)
        account.id = None
        with pytest.raises(DataValidationError):
            account.update()

    def test_delete_account(self):
        """Prueba la eliminación de una cuenta utilizando datos conocidos"""
        random_key = random.randint(0, len(ACCOUNT_DATA) - 1)# usa import random
        data = ACCOUNT_DATA[random_key]  # obtener una cuenta aleatoria
        account = Account(**data)
        account.create()
        assert len(Account.all()) == 1
        account.delete()
        assert len(Account.all()) == 0
