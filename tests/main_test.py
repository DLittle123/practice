import pytest

from main import *
from utilities.seating_utilities import load_table_info, load_party_info
from utilities.utilities import sorter

big_table = [ {'name': 'A', 'size_remaining': 8, 'parties': []}, 
              {'name': 'B', 'size_remaining': 8, 'parties': []}, 
              {'name': 'C', 'size_remaining': 7, 'parties': []}, 
              {'name': 'D', 'size_remaining': 7, 'parties': []}]
small_table = [ {'name': 'C', 'size_remaining': 7, 'parties': []}, 
                {'name': 'D', 'size_remaining': 7, 'parties': []},
                {'name': 'A', 'size_remaining': 8, 'parties': []}, 
                {'name': 'B', 'size_remaining': 8, 'parties': []}]
normal_party = [{'name': 'Reese', 'size': 7}, 
                {'name': 'Owens', 'size': 6, 'dislikes': 'Thornton, Taylor'}, 
                {'name': 'Taylor', 'size': 5}, 
                {'name': 'Thornton', 'size': 3}, 
                {'name': 'Garcia', 'size': 2}, 
                {'name': 'Smith', 'size': 1, 'dislikes': 'Garcia'}]
big_normal_expected = [ {'name': 'A', 'size_remaining': 0, 'parties': [{'name': 'Reese', 'size': 7}, {'name': 'Smith', 'size': 1, 'dislikes': 'Garcia'}]}, 
                        {'name': 'B', 'size_remaining': 0, 'parties': [{'name': 'Owens', 'size': 6, 'dislikes': 'Thornton, Taylor'}, {'name': 'Garcia', 'size': 2}]}, 
                        {'name': 'C', 'size_remaining': 2, 'parties': [{'name': 'Taylor', 'size': 5}]}, 
                        {'name': 'D', 'size_remaining': 4, 'parties': [{'name': 'Thornton', 'size': 3}]}]
small_normal_expected = [ {'name': 'C', 'size_remaining': 2, 'parties': [{'name': 'Thornton', 'size': 3}, {'name': 'Garcia', 'size': 2}]}, 
                          {'name': 'D', 'size_remaining': 0, 'parties': [{'name': 'Owens', 'size': 6, 'dislikes': 'Thornton, Taylor'}, {'name': 'Smith', 'size': 1, 'dislikes': 'Garcia'}]}, 
                          {'name': 'A', 'size_remaining': 3, 'parties': [{'name': 'Taylor', 'size': 5}]}, 
                          {'name': 'B', 'size_remaining': 1, 'parties': [{'name': 'Reese', 'size': 7}]}]

@pytest.mark.parametrize("tables, parties, expected", 
  [ (big_table, normal_party, big_normal_expected),
    (small_table, normal_party, small_normal_expected),
    ()])
def test_simple_solution():
   