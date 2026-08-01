
def _run_main(main, argv):
  """Calls main, optionally with a debugger or profiler."""
  if FLAGS.run_with_pdb:
    sys.exit(_get_debugger_module_with_function('runcall').runcall(main, argv))
  elif FLAGS.run_with_profiling or FLAGS.profile_file:
    # Avoid import overhead since most apps (including performance-sensitive
    # ones) won't be run with profiling.
    # pylint: disable=g-import-not-at-top
    import atexit
    if FLAGS.use_cprofile_for_profiling:
      import cProfile as profile
    else:
      import profile
    profiler = profile.Profile()
    if FLAGS.profile_file:
      atexit.register(profiler.dump_stats, FLAGS.profile_file)
    else:
      atexit.register(profiler.print_stats)
    sys.exit(profiler.runcall(main, argv))
  else:
    sys.exit(main(argv))

