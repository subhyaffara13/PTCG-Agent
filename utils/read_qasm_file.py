
def read_qasm_file(filename):
    return Qasm(*open(filename).readlines())

