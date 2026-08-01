
def show_runtime():
    """
    Print information about various resources in the system
    including available intrinsic support and BLAS/LAPACK library
    in use

    .. versionadded:: 1.24.0

    See Also
    --------
    show_config : Show libraries in the system on which NumPy was built.

    Notes
    -----
    1. Information is derived with the help of `threadpoolctl <https://pypi.org/project/threadpoolctl/>`_
       library if available.
    2. SIMD related information is derived from ``__cpu_features__``,
       ``__cpu_baseline__`` and ``__cpu_dispatch__``

    """
    from pprint import pprint

    from numpy._core._multiarray_umath import (
        __cpu_baseline__,
        __cpu_dispatch__,
        __cpu_features__,
    )
    config_found = [{
        "numpy_version": np.__version__,
        "python": sys.version,
        "uname": platform.uname(),
        }]
    features_found, features_not_found = [], []
    for feature in __cpu_dispatch__:
        if __cpu_features__[feature]:
            features_found.append(feature)
        else:
            features_not_found.append(feature)
    config_found.append({
        "simd_extensions": {
            "baseline": __cpu_baseline__,
            "found": features_found,
            "not_found": features_not_found
        }
    })
    config_found.append({
        "ignore_floating_point_errors_in_matmul":
            not np._core._multiarray_umath._blas_supports_fpe(None),
    })

    try:
        from threadpoolctl import threadpool_info
        config_found.extend(threadpool_info())
    except ImportError:
        print("WARNING: `threadpoolctl` not found in system!"
              " Install it by `pip install threadpoolctl`."
              " Once installed, try `np.show_runtime` again"
              " for more detailed build information")
    pprint(config_found)

