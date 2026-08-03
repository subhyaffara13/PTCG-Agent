import sys

def _is_jax_array(x):
    """Return whether *x* is a JAX Array."""
    try:
        # We're intentionally not attempting to import jax. If somebody
        # has created a jax array, jax should already be in sys.modules.
        tp = sys.modules.get("jax").Array
    except AttributeError:
        return False  # Module not imported or a nonstandard module with no Array attr.
    return (isinstance(tp, type)  # Just in case it's a very nonstandard module.
            and isinstance(x, tp))

