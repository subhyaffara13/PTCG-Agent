
def get_float32_precision():
    if (
        (
            torch.backends.cuda.matmul.fp32_precision == "ieee"
            if torch.backends.cuda.matmul.fp32_precision != "none"
            else torch.get_float32_matmul_precision() == "highest"
        )
        or torch.version.hip
        or torch.mtia.is_available()
    ):
        return "'ieee'"
    else:
        return "'tf32'"

