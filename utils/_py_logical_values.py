
def _py_logical_values(rbool):
    if rbool in ["TRUE", "T"]:
        return True
    if rbool in ["FALSE", "F"]:
        return False
    raise RLogicalValueError

