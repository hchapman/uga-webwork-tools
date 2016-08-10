#!/usr/bin/python

"""
wwconvert.py

Convert various UGA class roll data formats to standard WebWork .lst
for import.
"""

from __future__ import print_function
import csv

# Format of WebWork .lst for student import is
# [password],[lastname],[firstname],C,,,, [username]@uga.edu,[username]

def studentdict_to_webwork(sdict):
    """
    studentdict_to_webwork(sdict)

    Given a dict with keys {password, lastname, firstname, username},
    return a valid row for WebWork lst import. If data is incomplete,
    return None.
    """

    try:
        return ("{password},{lastname},{firstname}"
                ",C,,,,\t{username}@uga.edu,{username}").format(**sdict)
    except KeyError:
        return None

def uga_email_to_username(email):
    """
    uga_email_to_username(email)

    Given a UGA email "myid@uga.edu", return myid. We are probably
    guaranteed not to have any "\@" or other confusing characters.
    """

    # TODO: Make more robust but don't reinvent wheel...
    return email.split("@")[0]

def athena_fullname_to_lastname(fullname):
    """
    athena_fullname_to_lastname(fullname)

    Given fullname Lastname, Firstname, M., return the student's
    last name, usually "Lastname"
    """
    return fullname.split(",")[0]

def iterate_athena_csv_file(csvfile):
    """
    iterate_athena_csv_file(csvfile)

    Iterates through list of {password, lastname, firstname, myid}, one
    per student, for conversion to WebWork format
    """

    # First row of Athena CSV file is header row
    # Important columns of Athena CSV file are (0-indexed):
    # 1: Preferred first name; we use this as firstname
    # 2: Last, First, M.; we grab up to the comma as lastname
    # 3: UGA ID; we use this as password
    # 9: Email in fmt [username]@uga.edu; grepped appropriately
    athreader = csv.reader(csvfile)
    header = athreader.next() # Grab the header row
    for row in athreader:
        yield {
            'password': row[3],
            'lastname': athena_fullname_to_lastname(row[2]),
            'firstname': row[1],
            'username': uga_email_to_username(row[9]),
        }

def convert_athena_csv_file(f):
    """
    convert_athena_csv_file(f)

    Given an Athena CSV file, return a string in WebWork
    .lst format that we expect.
    """

    lstdata = []
    for student in iterate_athena_csv_file(f):
        lststudent = studentdict_to_webwork(student)
        lstdata.append(lststudent)
    return lstdata

def save_webwork_lst(lstdata, ofile):
    """
    save_webwork_lst(lstdata, ofile)

    Save webwork list data (lines in a list, lstdata) to ofile
    (possibly stdout)
    """
    for line in lstdata:
        print(line, file=ofile)

if __name__ == "__main__":
    # Run as a script
    import argparse
    import sys

    parser = argparse.ArgumentParser(
        description="Convert various UGA data formats to WW .lst")

    parser.add_argument("-o", "--outfile", type=argparse.FileType('w'),
                        help="File to save to. Default: stdout",
                        default=sys.stdout)

    parser.add_argument("file", nargs="?", type=argparse.FileType('rb'),
                        help="File to parse.",
                        default=sys.stdin)

    args = parser.parse_args()
    lstdata = convert_athena_csv_file(args.file)

    save_webwork_lst(lstdata, args.outfile)
