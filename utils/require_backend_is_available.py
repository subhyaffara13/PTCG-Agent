
def require_backend_is_available(backends):
    def check(backend):
        if backend == dist.Backend.GLOO:
            return dist.is_gloo_available()
        if backend == dist.Backend.NCCL:
            return dist.is_nccl_available()
        if backend == dist.Backend.MPI:
            return dist.is_mpi_available()
        if backend == dist.Backend.UCC:
            return dist.is_ucc_available()
        if backend in DistTestCases.backend_feature["plugin"]:
            return True
        return False

    if BACKEND not in backends:
        return skip_but_pass_in_sandcastle(
            f"Test requires backend {BACKEND} to be one of {backends}"
        )

    if not check(dist.Backend(BACKEND)):
        return skip_but_pass_in_sandcastle(
            f"Test requires backend {BACKEND} to be available"
        )
    return lambda func: func

