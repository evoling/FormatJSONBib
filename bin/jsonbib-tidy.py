#!/usr/bin/env python3
import json
import argparse
import sys
"""
Filter unnecessary fields from json bibliography files
Add `file` fields for pdfs with matching basename
"""

keep_fields = {
        u'DOI',
        # u'ISBN',
        # u'ISSN',
        u'URL',
        # u'abstract',
        # u'accessed',
        u'author',
        u'collection-title',
        u'container-title',
        u'editor',
        # u'event-place',
        u'genre',
        # u'id',
        # u'issue',
        u'issued',
        # u'journalAbbreviation',
        # u'language',
        # u'note',
        # u'number-of-pages',
        u'page',
        u'publisher',
        u'publisher-place',
        # u'shortTitle',
        # u'source',
        u'title',
        u'type',
        u'volume'}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bibfiles", type=open, nargs="+", help="JSON files")
    # parser.add_argument("-p", "--pdfdir", type=is_dir, default="/pdf",
    #         help="""path to files in server root (files under
    #         `/pdf/*.pdf` on the server correspond to file stored `files/pdf`
    #         in nikola)""")
    parser.add_argument("-n", "--dry-run", action="store_true")
    args = parser.parse_args()
    pubs = list()
    for fileobj in args.bibfiles:
        item = json.load(fileobj)
        filename = fileobj.name
        fileobj.close()
        for key in list(item.keys()): # ensure it's a dict
            if key not in keep_fields:
                if args.dry_run:
                    print(filename, "drop field", key)
                item.pop(key)
        if not args.dry_run:
            with open(filename, "w") as fileobj:
                json.dump(item, fileobj)
            

if __name__ == "__main__":
    main()
