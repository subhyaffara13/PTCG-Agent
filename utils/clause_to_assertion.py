
def clause_to_assertion(clause):
    clause_strings = [f"d{abs(lit)}" if lit > 0 else f"(not d{abs(lit)})" for lit in clause]
    return "(assert (or " + " ".join(clause_strings) + "))"

