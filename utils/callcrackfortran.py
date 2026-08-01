
def callcrackfortran(files, options):
    rules.options = options
    crackfortran.debug = options['debug']
    crackfortran.verbose = options['verbose']
    if 'module' in options:
        crackfortran.f77modulename = options['module']
    if 'skipfuncs' in options:
        crackfortran.skipfuncs = options['skipfuncs']
    if 'onlyfuncs' in options:
        crackfortran.onlyfuncs = options['onlyfuncs']
    crackfortran.include_paths[:] = options['include_paths']
    crackfortran.dolowercase = options['do-lower']
    postlist = crackfortran.crackfortran(files)
    if 'signsfile' in options:
        outmess(f"Saving signatures to file \"{options['signsfile']}\"\n")
        pyf = crackfortran.crack2fortran(postlist)
        if options['signsfile'][-6:] == 'stdout':
            sys.stdout.write(pyf)
        else:
            with open(options['signsfile'], 'w') as f:
                f.write(pyf)
    if options["coutput"] is None:
        for mod in postlist:
            mod["coutput"] = f"{mod['name']}module.c"
    else:
        for mod in postlist:
            mod["coutput"] = options["coutput"]
    if options["f2py_wrapper_output"] is None:
        for mod in postlist:
            mod["f2py_wrapper_output"] = f"{mod['name']}-f2pywrappers.f"
    else:
        for mod in postlist:
            mod["f2py_wrapper_output"] = options["f2py_wrapper_output"]
    for mod in postlist:
        if options["requires_gil"]:
            mod['gil_used'] = 'Py_MOD_GIL_USED'
        else:
            mod['gil_used'] = 'Py_MOD_GIL_NOT_USED'
    # gh-26718 Reset global
    crackfortran.f77modulename = ''
    return postlist

