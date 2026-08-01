
def bmm_to_mm(match: Match, mat1: torch.fx.Node, mat2: torch.fx.Node):
    """Convert bmm to mm when batch size is 1"""

    def repl(a, b):
        return torch.mm(a.squeeze(0), b.squeeze(0)).unsqueeze(0)

    if (
        check_device(mat1.meta["val"], mat2.meta["val"], get_gpu_type())
        and statically_known_true(mat1.meta["val"].shape[0] == 1)
        and statically_known_true(mat2.meta["val"].shape[0] == 1)
    ):
        # pyrefly: ignore [bad-argument-type]
        match.replace_by_example(repl, [mat1, mat2])

