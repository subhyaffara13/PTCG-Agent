
def inherit_validators(base_validators: 'ValidatorListDict', validators: 'ValidatorListDict') -> 'ValidatorListDict':
    for field, field_validators in base_validators.items():
        if field not in validators:
            validators[field] = []
        validators[field] += field_validators
    return validators

