
def requires_mpi():
    return skip_but_pass_in_sandcastle_if(
        not c10d.is_mpi_available(),
        "c10d was not compiled with the MPI backend",
    )

