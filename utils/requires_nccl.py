
def requires_nccl():
    return skip_but_pass_in_sandcastle_if(
        not c10d.is_nccl_available(),
        "c10d was not compiled with the NCCL backend",
    )

