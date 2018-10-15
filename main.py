"""
Wedding seat planner
Author: David Little
"""
import re

"""
main controller
"""
def main():
  table_info = load_table_info()
  party_info = load_party_info()

  #all_solutions = generate_all_solutions(table_info.copy(), party_info.copy())


"""
Reads in the table info from a file
assumptions: 
  table info is always a single line
  'tables: ' is always at the head
  tables are defined as 'table_name-max_capacity' seperated by a space
"""

def load_table_info(filename='tables.txt'):
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

def load_party_info(filename='reservations.txt'):
  party_array = []
  for party in open("input_data/" + filename, "r"):
    split_party = re.split(r', party of | dislikes ', party.rstrip('\n'))
    party_info = { 'name': split_party[0], 'size': int(split_party[1]) }
    if len(split_party) == 3:
      party_info['dislikes'] = split_party[2]
    party_array.append(party_info)
  return party_array


"""
Simple solution
"""
def simple_solution(tables, parties):
  sorted_tables = sorted(tables, key=lambda k: k['size_remaining'], reverse=True)
  sorted_parties = sorted(parties, key=lambda k: k['size'], reverse=True)
  for party in sorted_parties:
    for table in sorted_tables:
      if fits(party, table) and sits(party, table['parties']):
        table['parties'].append(party)
        table['size_remaining'] -= party['size']
        parties.remove(party)
        break;
  if parties:
    return False
  else:
    return sorted_tables


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
  solution_array = []


"""

"""



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





