
def list_to_dict(aList):
    return {nativestr(aList[i][0]): nativestr(aList[i][1]) for i in range(len(aList))}

