
def requires_nccl_version(version, msg):
    if not TEST_CUDA:
        return lambda f: f
    if not c10d.is_nccl_available():
        return skip_but_pass_in_sandcastle(
            "c10d was not compiled with the NCCL backend",
        )
    else:
        return skip_but_pass_in_sandcastle_if(
            torch.cuda.nccl.version() < version,
            f"Requires NCCL version greater than or equal to: {version}, found: {torch.cuda.nccl.version()}, reason: {msg}",
        )

