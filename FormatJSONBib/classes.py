#!/usr/bin/env python
import json

class Publication(object):

    def __init__(self, d):
        for key in d:
            if "-" in key:
                d[key.replace("-","_")] = d.pop(key)
        self.__dict__.update(d)
        try:
            assert self.author
        except AttributeError:
            raise AttributeError("No author in", self.__dict__)
        return

    def format_author(self):
        author_list = list()
        author_list.append("{family}, {given}".format(**self.author[0]))
        for author in self.author[1:]:
            author_list.append("{given} {family}".format(**author))
        return ", ".join(author_list)

    @property
    def date(self):
        return self.issued["date-parts"][0][0]

    def format_date(self):
        return "-".join([e[0] for e in self.issued["date-parts"]])

class Article(Publication):
    
    def render(self):

        return ("{author}. {date}. {title}. <i>{journal}</i>. "
                "{volume}, {issue}:{page}.").format(
                author=self.format_author(),
                date=self.format_date(),
                title=self.title,
                journal=self.container_title,
                volume=self.volume,
                issue=self.issue,
                page=self.page)

class Chapter(Publication):
    pass

class Thesis(Publication):
    pass

class UnknownPublicationType(Exception):
    pass

def constructor(jsonobj):
    classes = {
            "article-journal":Article,
            "chapter":Chapter,
            "thesis":Thesis,
            }
    pubtype = jsonobj.pop("type")
    try:
        return classes[pubtype](jsonobj)
    except KeyError:
        print("WARNING: unknown type", pubtype)
        raise UnknownPublicationType


