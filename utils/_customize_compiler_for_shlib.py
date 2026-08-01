
def _customize_compiler_for_shlib(compiler):
    if sys.platform == "darwin":
        # building .dylib requires additional compiler flags on OSX; here we
        # temporarily substitute the pyconfig.h variables so that distutils'
        # 'customize_compiler' uses them before we build the shared libraries.
        tmp = _CONFIG_VARS.copy()
        try:
            # XXX Help!  I don't have any idea whether these are right...
            _CONFIG_VARS['LDSHARED'] = (
                "gcc -Wl,-x -dynamiclib -undefined dynamic_lookup"
            )
            _CONFIG_VARS['CCSHARED'] = " -dynamiclib"
            _CONFIG_VARS['SO'] = ".dylib"
            customize_compiler(compiler)
        finally:
            _CONFIG_VARS.clear()
            _CONFIG_VARS.update(tmp)
    else:
        customize_compiler(compiler)

