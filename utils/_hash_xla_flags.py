
def _hash_xla_flags(hash_obj, extra_flag_prefixes: list[str]):
  xla_flags = []

  xla_flags_env_var = os.getenv("XLA_FLAGS")
  if xla_flags_env_var:
    xla_flags.extend(xla_flags_env_var.split())
  libtpu_init_args_env_var = os.getenv("LIBTPU_INIT_ARGS")
  if libtpu_init_args_env_var:
    xla_flags.extend(libtpu_init_args_env_var.split())

  for arg in sys.argv:
    if arg.startswith("--xla") or any(
        arg.startswith(p) for p in extra_flag_prefixes
    ):
      xla_flags.append(arg)

  # N.B. all XLA flags that take an argument must use '=' and not a space
  # (e.g. --xla_force_host_platform_device_count=8) (I think).
  for flag in sorted(xla_flags):
    if flag.split("=")[0] in xla_flags_to_exclude_from_cache_key:
      logger.debug("Not including XLA flag in cache key: %s", flag)
      continue
    logger.debug("Including XLA flag in cache key: %s", flag)
    _hash_string(hash_obj, flag)

