from to_glue import convert
from pydantic import BaseModel
from typing import List, Union


def test_empty():
    assert convert('') == []


def test_single_string_column():
    class A(BaseModel):
        name: str

    expected = [('name', 'string')]

    assert convert(A.schema_json()) == expected

def test_single_float_column():
    class A(BaseModel):
        name: float

    expected = [('name', 'float')]

    assert convert(A.schema_json()) == expected


def test_single_boolean_column():
    class A(BaseModel):
        name: bool

    expected = [('name', 'boolean')]

    assert convert(A.schema_json()) == expected


def test_multiple_string_column():
    class A(BaseModel):
        hey: str
        ho: str
        lets: str
        go: str

    expected = [
        ('hey', 'string'),
        ('ho', 'string'),
        ('lets', 'string'),
        ('go', 'string'),
    ]

    assert convert(A.schema_json()) == expected


def test_multiple_string_and_int_column():
    class A(BaseModel):
        hey: str
        ho: int
        lets: str
        go: int

    expected = [
        ('hey', 'string'),
        ('ho', 'int'),
        ('lets', 'string'),
        ('go', 'int'),
    ]

    assert convert(A.schema_json()) == expected


def test_nested_object_with_strings():
    class B(BaseModel):
        foo: str
        bar: str

    class A(BaseModel):
        some_b: B

    expected = [
        ('some_b', 'struct<foo:string,bar:string>'),
    ]

    assert convert(A.schema_json()) == expected

def test_nested_object_with_strings_and_ints():
    class B(BaseModel):
        foo: str
        x: int

    class A(BaseModel):
        one_b: B
        another_b: B
        some_number: int

    expected = [
        ('one_b', 'struct<foo:string,x:int>'),
        ('another_b', 'struct<foo:string,x:int>'),
        ('some_number', 'int'),
    ]

    assert convert(A.schema_json()) == expected


def test_list_of_ints():
    class A(BaseModel):
        nums: List[int]

    expected = [
        ('nums', 'array<int>'),
    ]

    assert convert(A.schema_json()) == expected


def test_list_of_ints_and_strings():
    class A(BaseModel):
        nums: List[int]
        strs: List[str]
        other: str

    expected = [
        ('nums', 'array<int>'),
        ('strs', 'array<string>'),
        ('other', 'string'),
    ]

    assert convert(A.schema_json()) == expected


def test_list_of_objects():
    class B(BaseModel):
        foo: str
        x: int

    class A(BaseModel):
        nums: List[int]
        boos: List[B]
        other: str

    expected = [
        ('nums', 'array<int>'),
        ('boos', 'array<struct<foo:string,x:int>>'),
        ('other', 'string'),
    ]

    assert convert(A.schema_json()) == expected

def test_union_of_string_and_int():
    class A(BaseModel):
        stuff: Union[str, int]

    expected = [
        ('stuff', 'union<string,int>')
    ]

    assert convert(A.schema_json()) == expected

def test_union_of_complex_types():
    class B(BaseModel):
        hey: str
        ho: str

    class C(BaseModel):
        lets: int
        go: int

    class A(BaseModel):
        stuff: Union[B, C]

    expected = [
        ('stuff', 'union<struct<hey:string,ho:string>,struct<lets:int,go:int>>')
    ]

    assert convert(A.schema_json()) == expected
