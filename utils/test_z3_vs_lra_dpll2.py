
def test_z3_vs_lra_dpll2():
    z3 = import_module("z3")
    if z3 is None:
        skip("z3 not installed.")

    def boolean_formula_to_encoded_cnf(bf):
        cnf = CNF.from_prop(bf)
        enc = EncodedCNF()
        enc.from_cnf(cnf)
        return enc

    def make_random_cnf(num_clauses=5, num_constraints=10, num_var=2):
        assert num_clauses <= num_constraints
        constraints = make_random_problem(num_variables=num_var, num_constraints=num_constraints, rational=False)
        clauses = [[cons] for cons in constraints[:num_clauses]]
        for cons in constraints[num_clauses:]:
            if isinstance(cons, Unequality):
                cons = ~cons
            i = randint(0, num_clauses-1)
            clauses[i].append(cons)

        clauses = [Or(*clause) for clause in clauses]
        cnf = And(*clauses)
        return boolean_formula_to_encoded_cnf(cnf)

    lra_dpll2_satisfiable = lambda x: dpll2_satisfiable(x, use_lra_theory=True)

    for _ in range(50):
        cnf = make_random_cnf(num_clauses=10, num_constraints=15, num_var=2)

        try:
            z3_sat = z3_satisfiable(cnf)
        except z3.z3types.Z3Exception:
            continue

        lra_dpll2_sat = lra_dpll2_satisfiable(cnf) is not False

        assert z3_sat == lra_dpll2_sat

