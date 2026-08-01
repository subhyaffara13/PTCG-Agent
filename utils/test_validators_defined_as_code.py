
def test_validators_defined_as_code():
    for param in rcsetup._params_list():
        validator = rcsetup._convert_validator_spec(param.name, param.validator)
        assert validator == rcsetup._validators[param.name]

