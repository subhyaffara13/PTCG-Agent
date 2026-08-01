
def requiresf90wrapper(rout):
    return ismoduleroutine(rout) or hasassumedshape(rout)

