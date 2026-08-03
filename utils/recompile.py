import os

def recompile(ffi, module_name, preamble, tmpdir='.', call_c_compiler=True,
              c_file=None, source_extension='.c', extradir=None,
              compiler_verbose=1, target=None, debug=None,
              uses_ffiplatform=True, **kwds):
    if not isinstance(module_name, str):
        module_name = module_name.encode('ascii')
    if ffi._windows_unicode:
        ffi._apply_windows_unicode(kwds)
    if preamble is not None:
        if call_c_compiler and _is_file_like(c_file):
            raise TypeError("Writing to file-like objects is not supported "
                            "with call_c_compiler=True")
        embedding = (ffi._embedding is not None)
        if embedding:
            ffi._apply_embedding_fix(kwds)
        if c_file is None:
            c_file, parts = _modname_to_file(tmpdir, module_name,
                                             source_extension)
            if extradir:
                parts = [extradir] + parts
            ext_c_file = os.path.join(*parts)
        else:
            ext_c_file = c_file
        #
        if target is None:
            if embedding:
                target = '%s.*' % module_name
            else:
                target = '*'
        #
        if uses_ffiplatform:
            ext = ffiplatform.get_extension(ext_c_file, module_name, **kwds)
        else:
            ext = None
        updated = make_c_source(ffi, module_name, preamble, c_file,
                                verbose=compiler_verbose)
        if call_c_compiler:
            patchlist = []
            cwd = os.getcwd()
            try:
                if embedding:
                    _patch_for_embedding(patchlist)
                if target != '*':
                    _patch_for_target(patchlist, target)
                if compiler_verbose:
                    if tmpdir == '.':
                        msg = 'the current directory is'
                    else:
                        msg = 'setting the current directory to'
                    print('%s %r' % (msg, os.path.abspath(tmpdir)))
                os.chdir(tmpdir)
                outputfilename = ffiplatform.compile('.', ext,
                                                     compiler_verbose, debug)
            finally:
                os.chdir(cwd)
                _unpatch_meths(patchlist)
            return outputfilename
        else:
            return ext, updated
    else:
        if c_file is None:
            c_file, _ = _modname_to_file(tmpdir, module_name, '.py')
        updated = make_py_source(ffi, module_name, c_file,
                                 verbose=compiler_verbose)
        if call_c_compiler:
            return c_file
        else:
            return None, updated

