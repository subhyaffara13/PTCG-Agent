
def idfn(x):
    xpr = re.compile(r"'(.*)?'")
    m = xpr.search(str(x))
    if m:
        return m.group(1)
    else:
        return str(x)

