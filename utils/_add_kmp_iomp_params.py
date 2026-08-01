
def _add_kmp_iomp_params(parser):
    group = parser.add_argument_group("IOMP Parameters")
    group.add_argument(
        "--disable-iomp",
        "--disable_iomp",
        action="store_true",
        default=False,
        help="By default, we use Intel OpenMP and libiomp5.so will be add to LD_PRELOAD",
    )

