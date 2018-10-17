"""
Returns magical digit string
Used in more than 1 place
Should always start with 0, otherwise padding gets weird
"""
def digit_string():
  return "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"


"""
Lifted from https://stackoverflow.com/questions/34030873/count-upward-in-python-with-variable-base
Essentially uses recursion to build up a string representing the number in a variable base
Works up to base26 (I hope we don't have more than 26 tables, otherwise we need to rejigger function)
"""
def int2str(x, base):
  digits = digit_string()
  if x < 0:
    return "-" + int2str(-x, base)
  return ("" if x < base else int2str(x//base, base)) + digits[x % base]


"""
adds left zero padding
"""
def padding(x, base, fill_to_size):
  return int2str(x, base).zfill(fill_to_size)


"""
sorter
"""
def sorter(list_, keyword, reverse=False):
  return sorted(list_, key=lambda k: k[keyword], reverse=reverse)