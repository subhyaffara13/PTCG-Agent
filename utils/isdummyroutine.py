
def isdummyroutine(rout):
    try:
        return rout['f2pyenhancements']['fortranname'] == ''
    except KeyError:
        return 0

