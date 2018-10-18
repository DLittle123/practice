This runs on python 3.6.3

To install dependencies for pytest

`pip3 install -r requirements.txt`

To run tests

`pytest` from the top directory

Wedding seat planner

Optional arguments `TABLENAME={filename in input_data} PARTYNAME={filename in input_data}`

To run

`{optional arguments} python3 main.py`


Also, this is a variation of the bin packing problem. 

The approach centers on running through 2 simple solutions first followed by a brute force solution


Futher enhancements:
 -  make padding function use whatever the zeroth index of digit_string is
 -  add error checking for loading the files
 -  Figure out a better way for main.py static values, either through refactoring methods in test or main file
 -  There is probably a better way instead of copy.deepcopy to reset stuff (maybe a helper function? loading the info each time?)