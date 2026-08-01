
def linalg_matrix_exp(self):
    squareCheckInputs(self, "linalg.matrix_exp")
    checkFloatingOrComplex(self, "linalg.matrix_exp")
    return torch.empty_like(self, memory_format=torch.contiguous_format)

