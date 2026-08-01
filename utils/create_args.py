
def create_args(parser=None):
    """
    Parse the command line options.

    @retval ArgumentParser
    """
    # pyrefly: ignore [missing-attribute]
    parser.add_argument(
        "--multi-instance",
        "--multi_instance",
        action="store_true",
        default=False,
        help="Enable multi-instance, by default one instance per node",
    )

    # pyrefly: ignore [missing-attribute]
    parser.add_argument(
        "-m",
        "--module",
        default=False,
        action="store_true",
        help="Changes each process to interpret the launch script "
        "as a python module, executing with the same behavior as"
        '"python -m".',
    )

    # pyrefly: ignore [missing-attribute]
    parser.add_argument(
        "--no-python",
        "--no_python",
        default=False,
        action="store_true",
        help='Do not prepend the --program script with "python" - just exec '
        "it directly. Useful when the script is not a Python script.",
    )

    _add_memory_allocator_params(parser)
    _add_kmp_iomp_params(parser)

    _add_multi_instance_params(parser)
    # positional
    # pyrefly: ignore [missing-attribute]
    parser.add_argument(
        "program",
        type=str,
        help="The full path to the program/script to be launched. "
        "followed by all the arguments for the script",
    )

    # rest from the training program
    # pyrefly: ignore [missing-attribute]
    parser.add_argument("program_args", nargs=REMAINDER)

