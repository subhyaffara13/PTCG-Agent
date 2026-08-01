
def upgrade_outputs(outputs):
    """upgrade outputs of a code cell from v3 to v4"""
    return [upgrade_output(op) for op in outputs]

