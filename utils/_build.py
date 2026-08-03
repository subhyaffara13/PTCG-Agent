import sys

def _build(tmpdir, ext, compiler_verbose=0, debug=None):
    # XXX compact but horrible :-(
    from cffi._shimmed_dist_utils import Distribution, CompileError, LinkError, set_threshold, set_verbosity

    dist = Distribution({'ext_modules': [ext]})
    dist.parse_config_files()
    options = dist.get_option_dict('build_ext')
    if debug is None:
        debug = sys.flags.debug
    options['debug'] = ('ffiplatform', debug)
    options['force'] = ('ffiplatform', True)
    options['build_lib'] = ('ffiplatform', tmpdir)
    options['build_temp'] = ('ffiplatform', tmpdir)
    #
    try:
        old_level = set_threshold(0) or 0
        try:
            set_verbosity(compiler_verbose)
            dist.run_command('build_ext')
            cmd_obj = dist.get_command_obj('build_ext')
            [soname] = cmd_obj.get_outputs()
        finally:
            set_threshold(old_level)
    except (CompileError, LinkError) as e:
        raise VerificationError('%s: %s' % (e.__class__.__name__, e))
    #
    return soname

