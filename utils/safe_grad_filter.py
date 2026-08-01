
def safe_grad_filter(message, category, filename, lineno, file=None, line=None) -> bool:
    return "The .grad attribute of a Tensor" not in str(message)

