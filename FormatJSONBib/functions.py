import json
import datetime
from sys import stdout, stderr
from textwrap import dedent
from os.path import join, basename, exists, abspath
from os import rename as osrename
from os import remove
from FormatJSONBib import *

def transform(args):
    pubs = list()
    for fileobj in args.files:
        jsonobj = json.load(fileobj)
        sentinel(jsonobj, fileobj.name)
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
    is_html = args.theme in ["bootstrap3", "plain"]

    if args.theme == "bootstrap3":
        print(dedent("""\
                <!--
                .. title: Publications
                .. slug: publications
                .. date: 
                .. tags:
                .. category:
                .. link:
                .. description:
                .. type: text
                -->
                """.format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))))
        print('<div class="list-group">')
    elif args.theme == "plain":
        print('<ul>')
    for pub in sorted(pubs, key=lambda p: ((-1 * p.date), p.format_author())):
        url = getattr(pub, "pdf_path", None)
        if not url:
            url = getattr(pub, "URL", "#")

        if args.theme == "bootstrap3":
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
        elif args.theme == "plain": # theme == plain
            print("<li>")
            print('{}. {}. {}.'.format(pub.format_author(),
                    pub.format_date(), 
                    pub.title))
            print(pub.format_source_html())
            if url != "#":
                print('<a href="{}" class="btn">'.format(url))
                if url.lower().endswith(".pdf"):
                    print('<span class="label label-success">pdf</span>')
                else:
                    print('<span class="label label-info">link</span>')
                print('</a>')
            print("</li>")
        elif args.theme == "markdown":
            print('{}. {}. {}. {}'.format(
                    pub.format_author())
                    pub.format_date(), 
                    pub.title,
                    pub.format_source_markdown())
            if url != "#":
                if url.lower().endswith(".pdf"):
                    print('(pdf)[{}]'.format(url))
                else:
                    print('(link)[{}]'.format(url))


    if args.theme == "bootstrap3":
        print('</div>')
    else: # theme == plain
        print('</ul>')
    return

def tidy(args):
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
        u'pdf_path', # custom field
        u'publisher',
        u'publisher-place',
        u'shortTitle',
        # u'source',
        u'title',
        u'type',
        u'volume'}
    pubs = list()
    for fileobj in args.files:
        item = json.load(fileobj)
        sentinel(item, fileobj.name)
        filename = fileobj.name
        fileobj.close()
        if args.drop_unused:
            for key in list(item.keys()): # ensure it's a dict
                if key not in keep_fields:
                    if args.dry_run:
                        print(filename, "drop field", key)
                    item.pop(key)
        if args.minify:
            separators = (",", ":")
            indent = None
        else:
            separators = (", ", ": ")
            indent = 4
        if not args.dry_run:
            with open(filename, "w") as fileobj:
                json.dump(item, fileobj, sort_keys=True, indent=indent,
                        separators=separators)
        else:
            json.dump(item, stdout, sort_keys=True, indent=indent,
                    separators=separators)
            print()
    return

def pdflink(args):
    pdfpath, filedir = abspath(args.pdfpath), abspath(args.filedir)
    assert pdfpath.startswith(filedir)
    relpath = join(".", pdfpath[len(filedir):])
    with open(args.jsonpath) as fileobj:
        data = json.load(fileobj)
        sentinel(data, fileobj.name)
        data["pdf_path"] = join(relpath, basename(args.pdfpath))
    with open(args.jsonpath, "w") as fileobj:
        json.dump(data, fileobj, indent=4, sort_keys=True)
    return

def rename(args):
    for fileobj in args.files:
        jsonobj = json.load(fileobj)
        sentinel(jsonobj, fileobj.name)
        try:
            bibobj = constructor(jsonobj)
            source = fileobj.name
            destination = bibobj.format_basename() + ".json"
            print("--> rename:", source, destination, file=stderr)
            if not args.dry_run:
                fileobj.close()
                osrename(source, destination)
        except UnknownPublicationType:
            print("Warning: Can't rename unknown type")
        except InvalidPublicationData:
            print("Warning: Can't rename invalid data")
    return

def split(args):
    items = json.load(args.file)
    jsonfilename = args.file.name
    args.file.close()
    i = 0
    try:
        assert type(items) == list
        for item in items:
            filename = "item-{:02}.json".format(i)
            while exists(filename):
                i += 1
                filename = "item-{:02}.json".format(i)
            json.dump(item, open(filename, "w"), indent=4, sort_keys=True)
            i += 1
        if args.delete:
            remove(jsonfilename)
    except AssertionError:
        print("Nothing to split:", jsonfilename, file=stderr)

def sentinel(data, name):
    """Test that data if a valid bibliography object"""
    try:
        msg = ("File {} is not an individual bibliography file (might "
                "need 'split')".format( name))
        assert type(data) == dict
        msg = "File {} is missing a title field".format(name)
        assert "title" in data
    except:
        raise InvalidPublicationData(msg)
