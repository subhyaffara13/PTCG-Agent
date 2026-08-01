
def downgrade_outputs(outputs):
    """downgrade outputs of a code cell to v3 from v4"""
    return [downgrade_output(op) for op in outputs]

