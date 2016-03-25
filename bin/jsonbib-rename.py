#!/usr/bin/env python3
import json
import argparse
import sys
from os.path import exists
from os import rename
from FormatJSONBib import *

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bibfiles", type=open, nargs="+", help="JSON files")
    parser.add_argument("-n", "--dry-run", action="store_true")
    args = parser.parse_args()

    for fileobj in args.bibfiles:
        jsonobj = json.load(fileobj)
        try:
            bibobj = constructor(jsonobj)
            source = fileobj.name
            destination = bibobj.format_basename() + ".json"
            print("--> mv", source, destination)
            if not args.dry_run:
                fileobj.close()
                rename(source, destination)
        except UnknownPublicationType:
            print("Warning: Can't rename unknown type")
        except InvalidPublicationData:
            print("Warning: Can't rename invalid data")

if __name__ == "__main__":
    main()
