
def test_pre_generated_assumption_rules_are_valid():
    # check the pre-generated assumptions match freshly generated assumptions
    # if this check fails, consider updating the assumptions
    # see sympy.core.assumptions._generate_assumption_rules
    pre_generated_assumptions =_load_pre_generated_assumption_rules()
    generated_assumptions =_generate_assumption_rules()
    assert pre_generated_assumptions._to_python() == generated_assumptions._to_python(), "pre-generated assumptions are invalid, see sympy.core.assumptions._generate_assumption_rules"

