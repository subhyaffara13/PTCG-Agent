
def _get_validators(cls: 'DataclassClassOrWrapper') -> 'CallableGenerator':
    yield cls.__validate__

