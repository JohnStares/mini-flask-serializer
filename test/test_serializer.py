import pytest

import sys
import os

PROJECT_ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT_DIR)

from .mock_db import Database1, Database2, Database3

from mini_flask_serializer import MiniFlaskSerializer
from mini_flask_serializer.exception import ValidationError

@pytest.fixture
def san():
    miniser = MiniFlaskSerializer()
    yield miniser

    miniser.serialize.clear()


def test_with_dict(san):
    db = Database1(1, "john", "john@gmail.com", "123456")

    assert san.serializer(db) == {
        "id": 1,
        "name": "john",
        "email": "john@gmail.com",
        "password": "123456"
    }

def test_with_json(san):
    db = Database2(2, "empress", "empress@gmail.com", "1234")

    assert san.serializer(db) == {
        "id": 2,
        "name": "empress",
        "email": "empress@gmail.com",
        "password": "1234",
    }


def test_alone(san):
    db = Database3(3, "ruth", "ruth@gmail.com", "1234567")

    assert san.serializer(db) == {
        "id": 3,
        "name": "ruth",
        "email": "ruth@gmail.com",
        "password": "1234567"
    }


def test_with_excluding_fields(san):
    db = Database3(3, "ruth", "ruth@gmail.com", "1234567")

    assert san.serializer(db, exclude_fields=["id"]) == {
        "name": "ruth",
        "email": "ruth@gmail.com",
        "password": "1234567"
    }

def test_with_including_fields(san):
    db = Database1(3, "ruth", "ruth@gmail.com", "1234567")

    assert san.serializer(db,include_fields=["name", "email", "password"]) == {
        "name": "ruth",
        "email": "ruth@gmail.com",
        "password": "1234567"
    }


def test_with_both_excluding_and_including_fields(san):
    db = Database2(3, "ruth", "ruth@gmail.com", "1234567")

    assert san.serializer(db, include_fields=["id", "name", "email", "password"], exclude_fields=["id", "password"]) != {
        "id": 3,
        "name": "ruth",
        "email": "ruth@gmail.com",
        "password": "1234567"
    }

    assert san.serializer(db, include_fields=["id", "name", "email", "password"], exclude_fields=["id", "password"]) == {
        "name": "ruth",
        "email": "ruth@gmail.com"
    }


def test_with_many_features(san):
    db = [Database1(1, "john", "john@gmail.com", "123456"), Database1(2, "empress", "empress@gmail.com", "123456"), Database1(3, "ruth", "ruth@gmail.com", "123456")]


    assert {
        "id": 4,
        "name": "emma",
        "email": "emma@gmail.com",
        "password": "1234567"
    } not in san.serializer(db, many=True)

    assert san.serializer(db, many=True) == [{
        "id": 1,
        "name": "john",
        "email": "john@gmail.com",
        "password": "123456"
    },
        {
        "id": 2,
        "name": "empress",
        "email": "empress@gmail.com",
        "password": "123456"
    },
     {
        "id": 3,
        "name": "ruth",
        "email": "ruth@gmail.com",
        "password": "123456"
    }]


def test_validate_data_agasints_api_fields_and_expected_fields(san):
    #fields your api sends
    api_fields = {
        "id": 1,
        "name": "john",
        "email": "john@gmail.com",
        "password": "123456"
    }

    #fields you are expecting from your api
    expected_fields = {
        "id": 1,
        "name": "john",
        "email": "john@gmail.com",
        "password": "123456"
    }

    assert san.validate_data(fields=api_fields, expected_fields=expected_fields) == {
        "id": 1,
        "name": "john",
        "email": "john@gmail.com",
        "password": "123456"
    }


def test_validate_data_agasints_api_fields_and_expected_fields_1(san):
    #fields your api sends
    api_fields = {
        "name": "john",
        "email": "john@gmail.com",
        "password": "123456"
    }

    #fields you are expecting from your api
    expected_fields = {
        "name": "john",
        "email": "john@gmail.com",
        "password": "123456"
    }

    assert san.validate_data(fields=api_fields, expected_fields=expected_fields) == {
        "name": "john",
        "email": "john@gmail.com",
        "password": "123456"
    }


def test_validate_data_agasints_api_fields_and_expected_fields_2(san):
    #fields your api sends
    api_fields = {
        "name": "john",
        "email": "john@gmail.com",
        "password": "123456"
    }

    #fields you are expecting from your api
    expected_fields = {
        "id": 1,
        "name": "john",
        "email": "john@gmail.com",
        "password": "123456"
    }

    with pytest.raises(ValidationError, match="{'id'} field is required."):
        san.validate_data(fields=api_fields, expected_fields=expected_fields)


def test_validate_data_agasints_api_fields_and_expected_fields_3(san):
    #fields your api sends
    api_fields = {
        "id": 1,
        "name": "john",
        "email": "john@gmail.com",
        "password": "123456"
    }

    #fields you are expecting from your api
    expected_fields = {
        "name": "john",
        "email": "john@gmail.com",
        "password": "123456"
    }

    with pytest.raises(ValidationError, match="{'id'} is not an expected field."):
        san.validate_data(fields=api_fields, expected_fields=expected_fields)


def test_validate_data_agasints_api_fields(san):
    #fields your api sends
    api_fields = {
        "name": "",
        "email": "john@gmail.com",
        "password": "123456"
    }

    with pytest.raises(ValidationError, match="name can't be empty."):
        san.validate_data(fields=api_fields)

    with pytest.raises(ValidationError, match="name can't be empty."):
        san.validate_data(fields={"name": " ", "email": "john@gmail.com", "password": "123456"})
    with pytest.raises(ValidationError, match="name is too short."):
        san.validate_data(fields={"name": "Jo", "email": "john@gmail.com", "password": "123456"})

    with pytest.raises(ValidationError, match="name cannot start with an underscore _ or hypen -."):
        san.validate_data(fields={"-name": "John", "email": "john@gmail.com", "password": "123456"})

    with pytest.raises(ValidationError, match="name cannot start with an underscore _ or hypen -."):
        san.validate_data(fields={"_name": "John", "email": "john@gmail.com", "password": "123456"})