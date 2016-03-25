
pubs = list()
for jsonobj in json.load(open("CV.json")):
    try:
        pubs.append(constructor(jsonobj))
    except UnknownPublicationType:
        pass
    except AttributeError:
        pass
