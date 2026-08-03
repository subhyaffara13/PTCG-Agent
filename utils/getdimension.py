import re

def getdimension(var):
    dimpattern = r"\((.*?)\)"
    if 'attrspec' in var.keys():
        if any('dimension' in s for s in var['attrspec']):
            return next(re.findall(dimpattern, v) for v in var['attrspec'])

