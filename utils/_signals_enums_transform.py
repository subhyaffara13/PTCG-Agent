
def _signals_enums_transform():
    """Generates the AST for 'Signals', 'Handlers' and 'Sigmasks' IntEnums."""
    return parse(_signals_enum() + _handlers_enum() + _sigmasks_enum())

