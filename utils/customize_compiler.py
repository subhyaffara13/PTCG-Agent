import os

def customize_compiler(compiler: CCompiler) -> None:
    """Do any platform-specific customization of a CCompiler instance.

    Mainly needed on Unix, so we can plug in the information that
    varies across Unices and is stored in Python's Makefile.
    """
    if compiler.compiler_type in ["unix", "cygwin"] or (
        compiler.compiler_type == "mingw32" and is_mingw()
    ):
        _customize_macos()

        (
            cc,
            cxx,
            cflags,
            ccshared,
            ldshared,
            ldcxxshared,
            shlib_suffix,
            ar,
            ar_flags,
        ) = get_config_vars(
            'CC',
            'CXX',
            'CFLAGS',
            'CCSHARED',
            'LDSHARED',
            'LDCXXSHARED',
            'SHLIB_SUFFIX',
            'AR',
            'ARFLAGS',
        )

        cxxflags = cflags

        if 'CC' in os.environ:
            newcc = os.environ['CC']
            if 'LDSHARED' not in os.environ and ldshared.startswith(cc):
                # If CC is overridden, use that as the default
                #       command for LDSHARED as well
                ldshared = newcc + ldshared[len(cc) :]
            cc = newcc
        cxx = os.environ.get('CXX', cxx)
        ldshared = os.environ.get('LDSHARED', ldshared)
        ldcxxshared = os.environ.get('LDCXXSHARED', ldcxxshared)
        cpp = os.environ.get(
            'CPP',
            cc + " -E",  # not always
        )

        ldshared = _add_flags(ldshared, 'LD')
        ldcxxshared = _add_flags(ldcxxshared, 'LD')
        cflags = os.environ.get('CFLAGS', cflags)
        ldshared = _add_flags(ldshared, 'C')
        cxxflags = os.environ.get('CXXFLAGS', cxxflags)
        ldcxxshared = _add_flags(ldcxxshared, 'CXX')
        cpp = _add_flags(cpp, 'CPP')
        cflags = _add_flags(cflags, 'CPP')
        cxxflags = _add_flags(cxxflags, 'CPP')
        ldshared = _add_flags(ldshared, 'CPP')
        ldcxxshared = _add_flags(ldcxxshared, 'CPP')

        ar = os.environ.get('AR', ar)

        archiver = ar + ' ' + os.environ.get('ARFLAGS', ar_flags)
        cc_cmd = cc + ' ' + cflags
        cxx_cmd = cxx + ' ' + cxxflags

        compiler.set_executables(
            preprocessor=cpp,
            compiler=cc_cmd,
            compiler_so=cc_cmd + ' ' + ccshared,
            compiler_cxx=cxx_cmd,
            compiler_so_cxx=cxx_cmd + ' ' + ccshared,
            linker_so=ldshared,
            linker_so_cxx=ldcxxshared,
            linker_exe=cc,
            linker_exe_cxx=cxx,
            archiver=archiver,
        )

        if 'RANLIB' in os.environ and compiler.executables.get('ranlib', None):
            compiler.set_executables(ranlib=os.environ['RANLIB'])

        compiler.shared_lib_extension = shlib_suffix

