#!/usr/bin/env python3
import json
import argparse
import datetime
from textwrap import dedent
import sys
from FormatJSONBib import *
"""
1. Export bibliographic data from Zotero in CSL JSON format

2. Split the exported file into separate json files, one per publication::

    jsonbib-split.py -d EXPORTED_FILE.json

3. Drop extra fields fields where appropriate::

    jsonbib-tidy.py *.json

   Add a "pdf_path" relative to server root for locally served pdfs

    .., "pdf_path":"/pdfs/filename.pdf"}

   (assuming a file stored in nikola files/pdfs/filename.pdf)

4. Generate html and move to pages directory::

    jsonbib2html.py -ui *.json > publications.html
    mv publications.html ../../evoling.github.io/pages/
"""


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", type=open, nargs="+", help="JSON files")
    parser.add_argument("-u", "--skip-unknown", action="store_true",
            help="Skip entries with unrecognised type")
    parser.add_argument("-i", "--skip-invalid", action="store_true",
            help="Skip entries that cannot be parsed")
    args = parser.parse_args()
    pubs = list()
    for fileobj in args.files:
        jsonobj = json.load(fileobj)
        try:
            bibobj = constructor(jsonobj)
            pubs.append(bibobj)
        except UnknownPublicationType:
            if args.skip_unknown:
                pass
            else:
                raise
        except InvalidPublicationData:
            if args.skip_invalid:
                pass
            else:
                raise

    print(dedent("""\
            <!--
            .. title: Publications
            .. slug: 
            .. date: 
            .. tags:
            .. category:
            .. link:
            .. description:
            .. type: text
            -->
            """.format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))))

    print('<div class="list-group">')
    for pub in sorted(pubs, key=lambda p: ((-1 * p.date), p.format_author())):
        url = getattr(pub, "pdf_path", None)
        if not url:
            url = getattr(pub, "URL", "#")
        print('<a href="{}" class="list-group-item">'.format(url))
        print('<h4 class="list-group-item-heading">{}</h4>'.format(
            pub.title))
        print('<p class="list-group-item-text">')
        print(pub.format_author())
        print('({})'.format(pub.format_date()))
        print(pub.format_source_html())
        if url == "#":
            pass
        elif url.lower().endswith(".pdf"):
            print('<span class="label label-success">pdf</span>')
        else:
            print('<span class="label label-info">link</span>')
        print('</p>')
        print('</a>')
    print('</div>')



if __name__ == "__main__":
    main()
