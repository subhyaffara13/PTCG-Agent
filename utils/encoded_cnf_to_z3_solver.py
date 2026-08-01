
def encoded_cnf_to_z3_solver(enc_cnf, z3):
    def dummify_bool(pred):
        return False
        assert isinstance(pred, AppliedPredicate)

        if pred.function in [Q.positive, Q.negative, Q.zero]:
            return pred
        else:
            return False

    s = z3.Solver()

    declarations = [f"(declare-const d{var} Bool)" for var in enc_cnf.variables]
    assertions = [clause_to_assertion(clause) for clause in enc_cnf.data]

    symbols = set()
    for pred, enc in enc_cnf.encoding.items():
        if not isinstance(pred, AppliedPredicate):
            continue
        if pred.function not in (Q.gt, Q.lt, Q.ge, Q.le, Q.ne, Q.eq, Q.positive, Q.negative, Q.extended_negative, Q.extended_positive, Q.zero, Q.nonzero, Q.nonnegative, Q.nonpositive, Q.extended_nonzero, Q.extended_nonnegative, Q.extended_nonpositive):
            continue

        pred_str = smtlib_code(pred, auto_declare=False, auto_assert=False, known_functions=known_functions)

        symbols |= pred.free_symbols
        pred = pred_str
        clause = f"(implies d{enc} {pred})"
        assertion = "(assert " + clause + ")"
        assertions.append(assertion)

    for sym in symbols:
        declarations.append(f"(declare-const {sym} Real)")

    declarations = "\n".join(declarations)
    assertions = "\n".join(assertions)
    s.from_string(declarations)
    s.from_string(assertions)

    return s

