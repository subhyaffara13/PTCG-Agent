
def requires_gloo():
    return skip_but_pass_in_sandcastle_if(
        not c10d.is_gloo_available(),
        "c10d was not compiled with the Gloo backend",
    )

