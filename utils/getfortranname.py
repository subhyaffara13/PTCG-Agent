
def getfortranname(rout):
    try:
        name = rout['f2pyenhancements']['fortranname']
        if name == '':
            raise KeyError
        if not name:
            errmess(f"Failed to use fortranname from {rout['f2pyenhancements']}\n")
            raise KeyError
    except KeyError:
        name = rout['name']
    return name

