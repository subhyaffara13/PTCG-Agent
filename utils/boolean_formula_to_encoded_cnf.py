
def boolean_formula_to_encoded_cnf(bf):
    cnf = CNF.from_prop(bf)
    enc = EncodedCNF()
    enc.from_cnf(cnf)
    return enc

