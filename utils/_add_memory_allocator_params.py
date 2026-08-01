
def _add_memory_allocator_params(parser):
    group = parser.add_argument_group("Memory Allocator Parameters")
    # allocator control
    group.add_argument(
        "--enable-tcmalloc",
        "--enable_tcmalloc",
        action="store_true",
        default=False,
        help="Enable tcmalloc allocator",
    )
    group.add_argument(
        "--enable-jemalloc",
        "--enable_jemalloc",
        action="store_true",
        default=False,
        help="Enable jemalloc allocator",
    )
    group.add_argument(
        "--use-default-allocator",
        "--use_default_allocator",
        action="store_true",
        default=False,
        help="Use default memory allocator",
    )

