
def z3_model_to_sympy_model(z3_model, enc_cnf):
    rev_enc = {value : key for key, value in enc_cnf.encoding.items()}
    return {rev_enc[int(var.name()[1:])] : bool(z3_model[var]) for var in z3_model}

