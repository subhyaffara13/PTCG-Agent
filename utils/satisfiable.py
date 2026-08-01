
def satisfiable(expr, algorithm=None, all_models=False, minimal=False, use_lra_theory=False):
    """
    Check satisfiability of a propositional sentence.
    Returns a model when it succeeds.
    Returns {true: true} for trivially true expressions.

    On setting all_models to True, if given expr is satisfiable then
    returns a generator of models. However, if expr is unsatisfiable
    then returns a generator containing the single element False.

    Examples
    ========

    >>> from sympy.abc import A, B
    >>> from sympy.logic.inference import satisfiable
    >>> satisfiable(A & ~B)
    {A: True, B: False}
    >>> satisfiable(A & ~A)
    False
    >>> satisfiable(True)
    {True: True}
    >>> next(satisfiable(A & ~A, all_models=True))
    False
    >>> models = satisfiable((A >> B) & B, all_models=True)
    >>> next(models)
    {A: False, B: True}
    >>> next(models)
    {A: True, B: True}
    >>> def use_models(models):
    ...     for model in models:
    ...         if model:
    ...             # Do something with the model.
    ...             print(model)
    ...         else:
    ...             # Given expr is unsatisfiable.
    ...             print("UNSAT")
    >>> use_models(satisfiable(A >> ~A, all_models=True))
    {A: False}
    >>> use_models(satisfiable(A ^ A, all_models=True))
    UNSAT

    """
    if use_lra_theory:
        if algorithm is not None and algorithm != "dpll2":
            raise ValueError(f"Currently only dpll2 can handle using lra theory. {algorithm} is not handled.")
        algorithm = "dpll2"

    if algorithm is None or algorithm == "pycosat":
        pycosat = import_module('pycosat')
        if pycosat is not None:
            algorithm = "pycosat"
        else:
            if algorithm == "pycosat":
                raise ImportError("pycosat module is not present")
            # Silently fall back to dpll2 if pycosat
            # is not installed
            algorithm = "dpll2"

    if algorithm=="minisat22":
        pysat = import_module('pysat')
        if pysat is None:
            algorithm = "dpll2"

    if algorithm=="z3":
        z3 = import_module('z3')
        if z3 is None:
            algorithm = "dpll2"

    if algorithm == "dpll":
        from sympy.logic.algorithms.dpll import dpll_satisfiable
        return dpll_satisfiable(expr)
    elif algorithm == "dpll2":
        from sympy.logic.algorithms.dpll2 import dpll_satisfiable
        return dpll_satisfiable(expr, all_models, use_lra_theory=use_lra_theory)
    elif algorithm == "pycosat":
        from sympy.logic.algorithms.pycosat_wrapper import pycosat_satisfiable
        return pycosat_satisfiable(expr, all_models)
    elif algorithm == "minisat22":
        from sympy.logic.algorithms.minisat22_wrapper import minisat22_satisfiable
        return minisat22_satisfiable(expr, all_models, minimal)
    elif algorithm == "z3":
        from sympy.logic.algorithms.z3_wrapper import z3_satisfiable
        return z3_satisfiable(expr, all_models)

    raise NotImplementedError

