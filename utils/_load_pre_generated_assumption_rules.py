
def _load_pre_generated_assumption_rules() -> FactRules:
    """ Load the assumption rules from pre-generated data

    To update the pre-generated data, see :method::`_generate_assumption_rules`
    """
    _assume_rules=FactRules._from_python(_assumptions)
    return _assume_rules

