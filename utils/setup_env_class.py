
def setup_env_class(builder: IRBuilder) -> ClassIR:
    """Generate a class representing a function environment.

    Note that the variables in the function environment are not
    actually populated here. This is because when the environment
    class is generated, the function environment has not yet been
    visited. This behavior is allowed so that when the compiler visits
    nested functions, it can use the returned ClassIR instance to
    figure out free variables it needs to access.  The remaining
    attributes of the environment class are populated when the
    environment registers are loaded.

    Return a ClassIR representing an environment for a function
    containing a nested function.
    """
    env_class = ClassIR(
        f"{builder.fn_info.namespaced_name()}_env",
        builder.module_name,
        is_generated=True,
        is_final_class=True,
    )
    env_class.reuse_freed_instance = True
    env_class.attributes[SELF_NAME] = RInstance(env_class)
    if builder.fn_info.is_nested and builder.fn_infos[-2]._env_class is not None:
        # If the function is nested, its environment class must contain an environment
        # attribute pointing to its encapsulating functions' environment class.
        env_class.attributes[ENV_ATTR_NAME] = RInstance(builder.fn_infos[-2].env_class)
    env_class.mro = [env_class]
    builder.fn_info.env_class = env_class
    builder.classes.append(env_class)
    return env_class

