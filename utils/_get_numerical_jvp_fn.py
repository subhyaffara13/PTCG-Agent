
def _get_numerical_jvp_fn(wrapped_fn, input_to_perturb, eps, nbhd_checks_fn):
    # Wraps jvp_fn so that certain arguments are already supplied
    def jvp_fn(delta):
        return _compute_numerical_gradient(
            wrapped_fn, input_to_perturb, delta, eps, nbhd_checks_fn
        )

    return jvp_fn

