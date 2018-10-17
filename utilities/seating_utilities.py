import re

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
  format is "party_name, party of {digit}, (dislikes party_name(, party_name)*)?"
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