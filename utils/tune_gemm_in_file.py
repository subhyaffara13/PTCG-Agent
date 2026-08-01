
def tune_gemm_in_file(filename: str) -> None:
    r"""tune GEMM in file."""

    if not is_enabled():
        raise AssertionError("TunableOp is not enabled")
    if not tuning_is_enabled():
        raise AssertionError("Tuning is not enabled")

    deviceid = torch.cuda.current_device()

    with open(filename) as file:
        for line in file:
            if line.startswith(("Gemm", "ScaledGemm")):
                _process_single_offline_gemm(line, deviceid)

