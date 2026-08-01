
def _docfill(obj, docdict, template=None):
    obj.__doc__ = doccer.docformat(template or obj.__doc__, docdict)

