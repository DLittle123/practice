import pytest
from utilities.seating_utilities import *

def test_load_table_info():
  tables = load_table_info('tables.txt')
  expected = [  {'name': 'A', 'size_remaining': 8, 'parties': []}, 
                {'name': 'B', 'size_remaining': 8, 'parties': []}, 
                {'name': 'C', 'size_remaining': 7, 'parties': []}, 
                {'name': 'D', 'size_remaining': 7, 'parties': []}]

  assert tables == expected


@pytest.mark.parametrize("filename, expected", 
  [ ('reservations.txt', [{'name': 'Thornton', 'size': 3}, 
                          {'name': 'Garcia', 'size': 2}, 
                          {'name': 'Owens', 'size': 6, 'dislikes': 'Thornton, Taylor'}, 
                          {'name': 'Smith', 'size': 1, 'dislikes': 'Garcia'}, 
                          {'name': 'Taylor', 'size': 5}, 
                          {'name': 'Reese', 'size': 7}]),
    ( 'reservations_pure_dislike.txt', 
      [ {'name': 'Thornton', 'size': 3, 'dislikes': 'Taylor, Garcia, Smith, Owens'}, 
        {'name': 'Garcia', 'size': 2, 'dislikes': 'Thornton, Taylor, Smith, Owens'}, 
        {'name': 'Owens', 'size': 6, 'dislikes': 'Thornton, Taylor, Garcia, Smith'}, 
        {'name': 'Smith', 'size': 1, 'dislikes': 'Thornton, Taylor, Garcia, Owens'}, 
        {'name': 'Taylor', 'size': 5, 'dislikes': 'Thornton, Garcia, Smith, Owens'}])])
def test_load_party_info(filename, expected):
  parties = load_party_info(filename)
  assert parties == expected


@pytest.mark.parametrize("party, table, expected",
  [ ({'size': '3'}, {'size_remaining': '4'}, True), 
    ({'size': 3}, {'size_remaining': '4'}, True), 
    ({'size': '3'}, {'size_remaining': 4}, True),
    ({'size': 3}, {'size_remaining': 4}, True),
    ({'size': '5'}, {'size_remaining': '3'}, False), 
    ({'size': 6}, {'size_remaining': '4'}, False), 
    ({'size': '17'}, {'size_remaining': 12}, False), 
    ({'size': '3'}, {'size_remaining': '3'}, True),
    ({'size': 3}, {'size_remaining': 3}, True)])
def test_fits(party, table, expected):
  assert fits(party, table) == expected


@pytest.mark.parametrize("party, table, expected",
  [ ({'name': 'Thornton', 'size': 3, 'dislikes': 'Owens'}, [{'name': 'Taylor', 'size': 5}, {'name': 'Reese', 'size': 7}], True),
    ({'name': 'Thornton', 'size': 3, 'dislikes': 'Taylor'}, [{'name': 'Taylor', 'size': 5}, {'name': 'Reese', 'size': 7}], False),
    ({'name': 'Thornton', 'size': 3, 'dislikes': 'Owens'}, [{'name': 'Taylor', 'size': 5, 'dislikes': 'Thornton'}, {'name': 'Reese', 'size': 7}], False),
    ({'name': 'Thornton', 'size': 3, 'dislikes': 'Owens'}, [], True),
    ({'name': 'Thornton', 'size': 3, 'dislikes': 'Taylor'}, [{'name': 'Taylor', 'size': 5, 'dislikes': 'Thornton'}, {'name': 'Reese', 'size': 7}], False)])
def test_sits(party, table, expected):
  assert sits(party, table) == expected


@pytest.mark.parametrize("tables, expected", 
  [ ([{'name': 'A', 'size_remaining': 0, 'parties': [{'name': 'Reese', 'size': 7}]}], "Table A: Reese, party of 7\n"),
    ([{'name': 'A', 'size_remaining': 0, 'parties': [{'name': 'Reese', 'size': 7}, {'name': 'Smith', 'size': 1, 'dislikes': 'Garcia'}]}], "Table A: Reese, party of 7 & Smith, party of 1\n"),
    ([{'name': 'A', 'size_remaining': 0, 'parties': []}], "Table A: Empty\n") ])
def test_pretty_print(tables, expected, capsys):
  pretty_print(tables)
  out = capsys.readouterr()
  assert out.out == expected