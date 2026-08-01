
def checkIsMatrix(A: Tensor, f_name: str, arg_name: str = "A"):
    torch._check(
        A.dim() >= 2,
        lambda: f"{f_name}: The input tensor {arg_name} must have at least 2 dimensions.",
    )


def check_is_matrix(A: TensorLikeType, f_name: str, arg_name: str = "A"):
    torch._check(
        len(A.shape) >= 2,
        lambda: f"{f_name}: The input tensor {arg_name} must have at least 2 dimensions.",
    )

