"""
Wedding seat planner
Author: David Little
"""
import re
import copy
import argparse
import os

"""
Reads in the table info from a file
assumptions: 
  table info is always a single line
  'tables: ' is always at the head
  tables are defined as 'table_name-max_capacity' seperated by a space
"""
def load_table_info(filename):
  with open("input_data/" + filename, "r") as input_tables:
    table_array = input_tables.readline().split(': ')[1].split(' ')
    #return { x.split('-')[0]: x.split('-')[1] for x in table_array }
    return list(map(lambda x: {'name': x.split('-')[0], 'size_remaining': int(x.split('-')[1]), 'parties': []}, table_array))


"""
Reads in party info from a file
assumptions:
  reservations info is always one party per line 
  format is "party_name, party of \d, (dislikes party_name(, party_name)*)?"
"""
def load_party_info(filename):
  party_array = []
  for party in open("input_data/" + filename, "r"):
    split_party = re.split(r', party of | dislikes ', party.rstrip('\n'))
    party_info = { 'name': split_party[0], 'size': int(split_party[1]) }
    if len(split_party) == 3:
      party_info['dislikes'] = split_party[2]
    party_array.append(party_info)
  return party_array


"""
sorter
"""
def sorter(list_, keyword, reverse=False):
  return sorted(list_, key=lambda k: k[keyword], reverse=reverse)


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
determines if there is enough space left at a table for the party
"""
def fits(party, table):
  return int(party['size']) <= int(table['size_remaining'])


"""
determines if we can have the party sit at the tables based on dislikes
"""
def sits(new_party, table_parties):
  valid = True
  for table_party in table_parties:
    if new_party['name'] in table_party.get('dislikes', '') or table_party['name'] in new_party.get('dislikes',''):
      valid = False
  return valid


"""
Generates all the possible solutions excluding dislikes
based on table size + party size
"""
def generate_all_solutions(tables, parties):
  digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
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
adds left zero padding
"""
def padding(x, base, fill_to_size):
  return int2str(x, base).zfill(fill_to_size)


"""
Lifted from https://stackoverflow.com/questions/34030873/count-upward-in-python-with-variable-base
Essentially uses recursion to build up a string representing the number in a variable base
Works up to base26 (I hope we don't have more than 26 tables, otherwise we need to rejigger function)
"""
def int2str(x, base):
  digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
  if x < 0:
    return "-" + int2str(-x, base)
  return ("" if x < base else int2str(x//base, base)) + digits[x % base]


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


"""
Formats a solution nicely for printing
"""
def pretty_print(solution):
  for table in solution:
    header = "Table {name}: ".format(name=table['name'])
    if table['parties']:
      party_string = ' & '.join(list("{name}, party of {size}".format(name=party['name'], size=party['size']) for party in table['parties']))
    else:
      party_string = 'Empty' 
    print(header+party_string)

if __name__ == "__main__":
  main(os.environ.get('PARTYNAME', 'reservations.txt'), os.environ.get('TABLENAME', 'tables.txt'))