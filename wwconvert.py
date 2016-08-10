#!/usr/bin/bash

"""
wwconvert.py

Convert various UGA class roll data formats to standard WebWork .lst
for import.
"""

import csv

# Format of WebWork .lst for student import is
# [password],[lastname],[firstname],C,,,, ,[myid]@uga.edu,,[myid]

def convert_athena_csv_file(fname):
    # First row of Athena CSV file is header row
    # Important columns of Athena CSV file are (0-indexed):
    # 
    with open(fname, 'rb') as csvfile:
        athreader = csv.reader(csvfile)

if __name__ == "__main__":
    # Run as a script
    import argparse
