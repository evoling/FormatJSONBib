#!/usr/bin/env python
from string import ascii_letters

class Publication(object):

    def __init__(self, d):
        for key, value in d.items():
            key = key.replace("-","_")
            setattr(self, key, value)
        try:
            assert self.author
        except AttributeError:
            raise InvalidPublicationData('No author in "{}"'.format(
                    d["title"]))
        return

    def format_author(self):
        author_list = list()
        author_list.append("{family}, {given}".format(**self.author[0]))
        for author in self.author[1:]:
            author_list.append("{given} {family}".format(**author))
        return ", ".join(author_list)

    def format_basename(self):
        elements = list()
        elements.append(self.author[0]["family"])
        if len(self.author) > 1:
            elements.append("et_al")
        elements.append(str(self.date))
        try:
            title = "".join([c for c in self.shortTitle if c in ascii_letters+" "])
        except AttributeError:
            title = "".join([c for c in self.title if c in ascii_letters+" "])
        elements.append("_".join(title.split()[:4]))
        return "_".join(elements)

    @property
    def date(self):
        """Date for sorting"""
        try:
            return int(self.issued["date-parts"][0][0])
        except ValueError:
            return self.issued["date-parts"][0][0]

    def format_date(self):
        return "-".join([e[0] for e in self.issued["date-parts"]])

    def __repr__(self):
        return '<{} "{}">'.format(self.__class__.__name__, self.title) 

class Article(Publication):
    
    def get_volume_issue(self):
        try:
            volume=self.volume
        except AttributeError:
            volume=None
        try:
            issue=self.issue
        except AttributeError:
            issue=None
        if volume and issue:
            return "{volume}, {issue}".format(volume=volume, issue=issue)
        else:
            return volume or issue or ""

    def render(self):

        return ("{author}. {date}. {title}. {journal}. "
                "{volumeissue}:{page}.").format(
                author=self.format_author(),
                date=self.format_date(),
                title=self.title,
                volumeissue=self.get_volume_issue(),
                journal=self.container_title,
                page=getattr(self, "page", ""))

    def format_source_html(self):

        return "<i>{journal}</i>. {volumeissue}:{page}.".format(
                author=self.format_author(),
                date=self.format_date(),
                title=self.title,
                volumeissue=self.get_volume_issue(),
                journal=self.container_title,
                page=getattr(self, "page", ""))

    def format_source_markdown(self):

        return "*{journal}*. {volumeissue}:{page}.".format(
                author=self.format_author(),
                date=self.format_date(),
                title=self.title,
                volumeissue=self.get_volume_issue(),
                journal=self.container_title,
                page=getattr(self, "page", ""))

class Chapter(Publication):

    def format_editor(self):
        editor_list = ["{given} {family}".format(**editor) for editor
                in self.editor]
        return ", ".join(editor_list)

    def format_source_html(self):

        return "In: {editor} ({eds}) {booktitle}. {publ}.  {page}".format(
                editor=self.format_editor(),
                eds="editors" if len(self.editor) > 1 else "editor",
                booktitle=self.container_title,
                publ=self.publisher,
                page=getattr(self, "page", ""))

    def format_source_markdown(self):

        return "In: {editor} ({eds}) {booktitle}. {publ}.  {page}".format(
                editor=self.format_editor(),
                eds="editors" if len(self.editor) > 1 else "editor",
                booktitle=self.container_title,
                publ=self.publisher,
                page=getattr(self, "page", ""))

class Thesis(Publication):

    def format_source_html(self):
        return "{genre} Dissertation, {university}.".format(
                genre=self.genre,
                university=self.publisher)

    def format_source_markdown(self):
        return "{genre} Dissertation, {university}.".format(
                genre=self.genre,
                university=self.publisher)

class UnknownPublicationType(Exception):
    pass

class InvalidPublicationData(Exception):
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
        raise UnknownPublicationType

