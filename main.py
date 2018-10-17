"""
Wedding seat planner
Author: David Little
"""
import copy
import os
from utilities.seating_utilities import *
from utilities.utilities import *

"""
main controller
"""
def main(partyname, tablename):
  solution = None
  
  table_info = load_table_info(tablename)
  party_info = load_party_info(partyname)
  
  sorted_tables_small_first = sorter(copy.deepcopy(table_info), 'size_remaining')
  sorted_tables_big_first = sorter(copy.deepcopy(table_info), 'size_remaining', reverse=True)
  sorted_parties = sorter(party_info, 'size', reverse=True)

  solution = simple_solution(sorted_tables_big_first.copy(), sorted_parties.copy())
  if not solution:
    solution = simple_solution(sorted_tables_small_first.copy(), sorted_parties.copy())
    if not solution:
      all_solutions = generate_all_solutions(copy.deepcopy(table_info), copy.deepcopy(party_info))
      solution = find_a_solution(all_solutions, table_info.copy())
  print(solution) if type(solution) == str else pretty_print(solution)


"""
Simple solution
"""
def simple_solution(tables, parties):
  tables_list = tables.copy()
  parties_list = parties.copy()
  for party in parties_list:
    for table in tables_list:
      if fits(party, table) and sits(party, table['parties']):
        table['parties'].append(party)
        table['size_remaining'] -= party['size']
        parties.remove(party)
        break;
  if parties:
    return False
  else:
    return tables_list


"""
Generates all the possible solutions excluding dislikes
based on table size + party size
"""
def generate_all_solutions(tables, parties):
  digits = digit_string()
  solution_array = []
  table_length = len(tables)
  party_length = len(parties)
  for x in range(0, table_length**party_length):
    solution_row = [[] for i in range(table_length)]
    seating_string = padding(x, table_length, party_length)
    for index, value in enumerate(seating_string):
      solution_row[digits.find(value)].append(parties[index].copy())
    solution_array.append(solution_row)
  return solution_array


"""
find the first solution that works from a solution array
"""
def find_a_solution(solution_array, tables):
  for solution in solution_array:
    table_copy = copy.deepcopy(tables)
    viable_solution = True
    for index, group in enumerate(solution):
      for party in group:
        if not fits(party, table_copy[index]) or not sits(party, table_copy[index]['parties']):
          viable_solution = False
        else:
          table_copy[index]['parties'].append(party)
          table_copy[index]['size_remaining'] -= party['size']
    if viable_solution:
      return table_copy
  return "No viable solution"


if __name__ == "__main__":
  main(os.environ.get('PARTYNAME', 'reservations.txt'), os.environ.get('TABLENAME', 'tables.txt'))