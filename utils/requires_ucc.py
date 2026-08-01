
def requires_ucc():
    return skip_but_pass_in_sandcastle_if(
        not c10d.is_ucc_available(),
        "c10d was not compiled with the UCC backend",
    )

