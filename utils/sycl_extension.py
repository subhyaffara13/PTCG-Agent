
def SyclExtension(name, sources, *args, **kwargs):
    r"""
    Creates a :class:`setuptools.Extension` for SYCL/C++.

    Convenience method that creates a :class:`setuptools.Extension` with the
    bare minimum (but often sufficient) arguments to build a SYCL/C++
    extension.

    All arguments are forwarded to the :class:`setuptools.Extension`
    constructor.

    .. warning::
        The PyTorch python API (as provided in libtorch_python) cannot be built
        with the flag ``py_limited_api=True``.  When this flag is passed, it is
        the user's responsibility in their library to not use APIs from
        libtorch_python (in particular pytorch/python bindings) and to only use
        APIs from libtorch (aten objects, operators and the dispatcher). For
        example, to give access to custom ops from python, the library should
        register the ops through the dispatcher.

        Contrary to CPython setuptools, who does not define -DPy_LIMITED_API
        as a compile flag when py_limited_api is specified as an option for
        the "bdist_wheel" command in ``setup``, PyTorch does! We will specify
        -DPy_LIMITED_API=min_supported_cpython to best enforce consistency,
        safety, and sanity in order to encourage best practices. To target a
        different version, set min_supported_cpython to the hexcode of the
        CPython version of choice.

    Example:
        >>> # xdoctest: +SKIP
        >>> # xdoctest: +REQUIRES(env:TORCH_DOCTEST_CPP_EXT)
        >>> from torch.utils.cpp_extension import BuildExtension, SyclExtension
        >>> setup(
        ...     name='xpu_extension',
        ...     ext_modules=[
        ...     SyclExtension(
        ...                 name='xpu_extension',
        ...                 sources=['extension.cpp', 'extension_kernel.cpp'],
        ...                 extra_compile_args={'cxx': ['-g', '-std=c++20', '-fPIC']})
        ...     ],
        ...     cmdclass={
        ...         'build_ext': BuildExtension
        ...     })

    By default the extension will be compiled to run on all archs of the cards visible during the
    building process of the extension. If down the road a new card is installed the
    extension may need to be recompiled. You can override the default behavior using
    `TORCH_XPU_ARCH_LIST` to explicitly specify which device architectures you want the extension
    to support:

    ``TORCH_XPU_ARCH_LIST="pvc,xe-lpg" python build_my_extension.py``

    Note that while it's possible to include all supported archs, the more archs get included the
    slower the building process will be, as it will build a separate kernel image for each arch.

    Note: Ninja is required to build SyclExtension.
    """
    library_dirs = kwargs.get("library_dirs", [])
    library_dirs += library_paths()
    kwargs["library_dirs"] = library_dirs

    libraries = kwargs.get("libraries", [])
    libraries.append("c10")
    libraries.append("c10_xpu")
    libraries.append("torch")
    libraries.append("torch_cpu")
    libraries.append("sycl")
    if not kwargs.get('py_limited_api', False):
        # torch_python uses more than the python limited api
        libraries.append("torch_python")
    libraries.append("torch_xpu")
    kwargs["libraries"] = libraries

    include_dirs = kwargs.get("include_dirs", [])
    include_dirs += include_paths(device_type="xpu")
    kwargs["include_dirs"] = include_dirs

    kwargs["language"] = "c++"

    return setuptools.Extension(name, sources, *args, **kwargs)

