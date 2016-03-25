#!/usr/bin/env python3
import json
import argparse
from os.path import exists
from os import remove
"""
Split a json bibliography into individual files, one per entry.
"""

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("jsonfile", type=open, help="JSON file")
    parser.add_argument("-d", "--delete", action="store_true",
            help="""Delete input file after splitting""")
    args = parser.parse_args()
    
    items = json.load(args.jsonfile)
    jsonfilename = args.jsonfile.name
    args.jsonfile.close()
    i = 0
    for item in items:
        filename = "item-{:02}.json".format(i)
        while exists(filename):
            i += 1
            filename = "item-{:02}.json".format(i)
        json.dump(item, open(filename, "w"))
        i += 1
    if args.delete:
        remove(jsonfilename)
                

if __name__ == "__main__":
    main()
