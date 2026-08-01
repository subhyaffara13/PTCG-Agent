
def _create_unary_propagating_op(name: str):
    def method(self):
        return pd_NA

    method.__name__ = name
    return method

