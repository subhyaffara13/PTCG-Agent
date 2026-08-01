
def _mat_mul_compatible(*args):
    """To check whether shapes are compatible for matrix mul."""
    return all(args[i].num_outputs == args[i+1].num_inputs for i in range(len(args)-1))

