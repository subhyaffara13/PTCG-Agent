
def linear_backward(input_, grad_output_, weight_, output_mask):
    grad_input = None
    grad_weight = None
    grad_bias = None
    if output_mask[0]:
        grad_input = grad_output_.new_empty(input_.size())
    if output_mask[1] or output_mask[2]:
        grad_weight = grad_output_.new_empty((grad_output_.size(-1), input_.size(-1)))
        grad_bias = grad_output_.new_empty(grad_output_.size(-1))
    return (grad_input, grad_weight, grad_bias)

