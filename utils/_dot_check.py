
def _dot_check(self, other):
    torch._check(
        self.dim() == 1 and other.dim() == 1,
        lambda: f"1D tensors expected, but got {self.dim()}D and {other.dim()}D tensors",
    )

    torch._check(
        self.dtype == other.dtype,
        lambda: "dot : expected both vectors to have same dtype, but found "
        f"{self.dtype} and {other.dtype}",
    )

    def numel_error():
        return (
            f"inconsistent tensor size, expected tensor [{self.numel()}] and src [{other.numel()}] to have the"
            f"same number of elements, but got {self.numel()} and {other.numel()} elements respectively"
        )

    torch._check(self.numel() == other.numel(), numel_error)

