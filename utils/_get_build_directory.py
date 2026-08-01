
def _get_build_directory(name: str, verbose: bool) -> str:
    """
    Get the build directory for an extension.

    Args:
        name: The name of the extension
        verbose: Whether to print verbose information

    Returns:
        The path to the build directory
    """
    root_extensions_directory = os.environ.get('TORCH_EXTENSIONS_DIR')
    if root_extensions_directory is None:
        root_extensions_directory = get_default_build_root()
        # Determine GPU accelerator prefix based on available accelerators. Fallback to CPU.
        # Priority: ROCm/HIP > CUDA > CPU
        # Note: torch.backends.cuda.is_built() returns True for both CUDA and ROCm,
        # so we need to check torch.version.hip to distinguish them
        if torch.version.hip is not None:
            accelerator_str = f'rocm{torch.version.hip.replace(".", "")}'
        elif torch.version.cuda is not None:
            accelerator_str = f'cu{torch.version.cuda.replace(".", "")}'
        else:
            accelerator_str = 'cpu'
        python_version = f'py{sys.version_info.major}{sys.version_info.minor}{getattr(sys, "abiflags", "")}'
        build_folder = f'{python_version}_{accelerator_str}'

        root_extensions_directory = os.path.join(
            root_extensions_directory, build_folder)

    if verbose:
        logger.info('Using %s as PyTorch extensions root...', root_extensions_directory)

    build_directory = os.path.join(root_extensions_directory, name)
    if not os.path.exists(build_directory):
        if verbose:
            logger.debug('Creating extension directory %s...', build_directory)
        # This is like mkdir -p, i.e. will also create parent directories.
        os.makedirs(build_directory, exist_ok=True)

    return build_directory

