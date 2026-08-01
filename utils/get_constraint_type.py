
def get_constraint_type(constraint):
    if isinstance(constraint, dict) and ("A" in constraint) and ("lb" in constraint) and ("ub" in constraint):
        return ConstraintType.LINEAR_DICT
    elif isinstance(constraint, dict) and ("fun" in constraint) and ("lb" in constraint) and ("ub" in constraint):
        return ConstraintType.NONLINEAR_DICT
    elif hasattr(constraint, "A") and hasattr(constraint, "lb") and hasattr(constraint, "ub"):
        return ConstraintType.LINEAR_OBJECT
    elif hasattr(constraint, "fun") and hasattr(constraint, "lb") and hasattr(constraint, "ub"):
        return ConstraintType.NONLINEAR_OBJECT
    else:
        raise ValueError(f"Constraint type {type(constraint)} not recognized")

