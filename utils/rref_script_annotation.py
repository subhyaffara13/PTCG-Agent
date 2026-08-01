
def rref_script_annotation(rref_var: RRef[Tensor]) -> Tensor:
    return rref_python_annotation(rref_var).to_here()

