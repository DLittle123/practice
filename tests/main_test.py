import pytest
from main import *

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
small_normal_expected = [ {'name': 'C', 'size_remaining': 0, 'parties': [{'name': 'Reese', 'size': 7}]}, 
                          {'name': 'D', 'size_remaining': 0, 'parties': [{'name': 'Owens', 'size': 6, 'dislikes': 'Thornton, Taylor'}, {'name': 'Smith', 'size': 1, 'dislikes': 'Garcia'}]}, 
                          {'name': 'A', 'size_remaining': 0, 'parties': [{'name': 'Taylor', 'size': 5}, {'name': 'Thornton', 'size': 3}]}, 
                          {'name': 'B', 'size_remaining': 6, 'parties': [{'name': 'Garcia', 'size': 2}]}]
tables_few_big = [{'name': 'A', 'size_remaining': 8, 'parties': []}, 
                  {'name': 'B', 'size_remaining': 4, 'parties': []}]
tables_few_small = [{'name': 'A', 'size_remaining': 4, 'parties': []}, 
                    {'name': 'B', 'size_remaining': 8, 'parties': []}]
party_few = [ {'name': 'Reese', 'size': 3},
              {'name': 'Owens', 'size': 7}]
party_dislikes = [{'name': 'Reese', 'size': 1, 'dislikes': 'Owens, Taylor'},
                  {'name': 'Owens', 'size': 1, 'dislikes': 'Taylor, Reese'},
                  {'name': 'Taylor', 'size': 1, 'dislikes': 'Owens, Reese'}]
small_solutions = [[[{'name': 'Reese', 'size': 3}, {'name': 'Owens', 'size': 7}], []],
                  [[{'name': 'Reese', 'size': 3}], [{'name': 'Owens', 'size': 7}]],
                  [[{'name': 'Owens', 'size': 7}], [{'name': 'Reese', 'size': 3}]],
                  [[], [{'name': 'Reese', 'size': 3}, {'name': 'Owens', 'size': 7}]]]

small_solution_answer_A = [ {'name': 'A', 'parties': [{'name': 'Owens', 'size': 7}], 'size_remaining': 1}, 
                            {'name': 'B', 'parties': [{'name': 'Reese', 'size': 3}], 'size_remaining': 1}]
small_solution_answer_B = [ {'name': 'A', 'parties': [{'name': 'Reese', 'size': 3}], 'size_remaining': 1}, 
                            {'name': 'B', 'parties': [{'name': 'Owens', 'size': 7}], 'size_remaining': 1}]
output_normal = 'Table A: Reese, party of 7 & Smith, party of 1\nTable B: Owens, party of 6 & Garcia, party of 2\nTable C: Taylor, party of 5\nTable D: Thornton, party of 3\n'


@pytest.mark.parametrize('tables, parties, expected', 
  [ (copy.deepcopy(big_table), copy.deepcopy(normal_party), big_normal_expected),
    (copy.deepcopy(small_table), copy.deepcopy(normal_party), small_normal_expected),
    (copy.deepcopy(tables_few_big), copy.deepcopy(party_few), False),
    (copy.deepcopy(tables_few_big), copy.deepcopy(party_dislikes), False)])
def test_simple_solution(tables, parties, expected):
   assert simple_solution(tables, parties) == expected

@pytest.mark.parametrize('tables, parties, expected, length',
  [ (copy.deepcopy(big_table), copy.deepcopy(normal_party), None, 4096),
    (copy.deepcopy(tables_few_big), copy.deepcopy(party_few), small_solutions, 4),
    (copy.deepcopy(big_table), copy.deepcopy(party_dislikes), None, 64)])
def test_generate_all_solutions(tables, parties, expected, length):
  if expected:
    assert generate_all_solutions(tables, parties) == expected
  assert len(generate_all_solutions(tables, parties)) == length


@pytest.mark.parametrize('solution_set, tables, expected',
  [ ([], copy.deepcopy(big_table), 'No viable solution'),
    (small_solutions, copy.deepcopy(tables_few_big), small_solution_answer_A),
    (small_solutions, copy.deepcopy(tables_few_small), small_solution_answer_B) ])
def test_find_a_solution(solution_set, tables, expected):
  assert find_a_solution(solution_set, tables) == expected


@pytest.mark.parametrize('reservation_name, expected',
  [ ('reservations.txt', output_normal), 
    ('reservations_pure_dislike.txt', 'No viable solution\n'),
    ('reservations_too_big.txt', 'No viable solution\n')])
def test_main(reservation_name, expected, capsys):
  main(reservation_name, 'tables.txt')
  out = capsys.readouterr()
  assert  out.out == expected


