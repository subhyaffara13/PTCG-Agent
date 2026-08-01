
def assert_correct_state(env_gym, env_name: str, state_jax: Any, atol: float = 1e-4):
    """Check that numpy-based env state is same as JAX dict."""

    state_gym = state_translate.np_state_to_jax(env_gym, env_name)
    # print(state_gym)
    # Loop over keys and assert that individual entries are same/close
    for k in state_gym.keys():
        jax_value = getattr(state_jax, k)
        # print(k, jax_value, state_gym[k])
        if k not in ["time", "terminal"]:
            if type(jax_value) in [
                jax.Array,
                # jaxlib.xla_extension.Buffer,
                jaxlib.xla_extension.ArrayImpl,
                np.ndarray,
            ]:
                assert np.allclose(jax_value, state_gym[k], atol=atol)
            else:
                # print(k, state_gym[k], state_jax[k])
                # Exclude extra time and terminal state from assertion
                if type(state_gym[k]) in [
                    float,
                    np.float64,
                    jax.Array,
                    # jaxlib.xla_extension.Buffer,
                    np.ndarray,
                    jaxlib.xla_extension.ArrayImpl,
                ]:
                    np.allclose(state_gym[k], jax_value, atol=atol)
                else:
                    print(type(state_gym[k]), k)
                    assert state_gym[k] == jax_value

