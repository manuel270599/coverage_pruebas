import random
import json
import pytest
import sys
import os
import datetime
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
