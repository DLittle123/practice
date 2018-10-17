import pytest
from utilities.utilities import *

def test_digit_string():
  assert type(digit_string()) == str

  #makes sure each char is unique since we use it for incrementing
  assert len(set(digit_string())) == len(digit_string())


@pytest.mark.parametrize('in1, in2, expected',
  [ (4, 2, '100'), 
    (16, 10, '16'),
    (16, 26, 'G')])
def test_int2str(in1, in2, expected):
  assert int2str(in1, in2) == expected


@pytest.mark.parametrize('in1, in2, fill, expected',
  [ (4, 2, 3, '100'),
    (4, 2, 5, '00100'),
    (16, 10, 2, '16'),
    (16, 10, 5, '00016'),
    (16, 26, 1, 'G'),
    (16, 26, 5, '0000G')])
def test_padding(in1, in2, fill, expected):
  assert padding(in1, in2, fill) == expected


def test_sorter():
  list_ = [ {'name': 'Foo', 'size': 2},
            {'name': 'Bar', 'size': 1},
            {'name': 'Baz', 'size': 4},
            {'name': 'Qux', 'size': 3}]
  keyword = 'size'

  list_final = [{'name': 'Bar', 'size': 1},
                {'name': 'Foo', 'size': 2},
                {'name': 'Qux', 'size': 3},
                {'name': 'Baz', 'size': 4}]

  assert sorter(list_, keyword) == list_final
  assert sorter(list_, keyword, False) == list_final
  assert sorter(list_, keyword, True) == list(reversed(list_final))