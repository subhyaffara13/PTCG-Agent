
def _make_capabilities_note(fun_name, capabilities, extra_note=None):
    if "out_of_scope" in capabilities:
        # It will be better to link to a section of the dev-arrayapi docs
        # that explains what is and isn't in-scope, but such a section
        # doesn't exist yet. Using :ref:`dev-arrayapi` as a placeholder.
        note = f"""
        **Array API Standard Support**

        `{fun_name}` is not in-scope for support of Python Array API Standard compatible
        backends other than NumPy.

        See :ref:`dev-arrayapi` for more information.
        """
        return textwrap.dedent(note)

    marray_note = (f"`{fun_name}` also accepts "
        "`MArrays <https://mdhaber.github.io/marray/tutorial.html>`__ "
        "backed by the backends indicated above; masked values will be treated as "
        "though they were not present." if capabilities.get("marray", False) else "")

    # Note: deliberately not documenting array-api-strict
    note = f"""
    **Array API Standard Support**

    `{fun_name}` has experimental support for Python Array API Standard compatible
    backends in addition to NumPy. Please consider testing these features
    by setting an environment variable ``SCIPY_ARRAY_API=1`` and providing
    CuPy, PyTorch, JAX, or Dask arrays as array arguments. The following
    combinations of backend and device (or other capability) are supported.

    ====================  ====================  ====================
    Library               CPU                   GPU
    ====================  ====================  ====================
    NumPy                 {capabilities['numpy']                   }
    CuPy                  {capabilities['cupy']                    }
    PyTorch               {capabilities['torch']                   }
    JAX                   {capabilities['jax.numpy']               }
    Dask                  {capabilities['dask.array']              }
    ====================  ====================  ====================

    {marray_note or ""}
    {extra_note or ""}
    See :ref:`dev-arrayapi` for more information.
    """

    return textwrap.dedent(note)

