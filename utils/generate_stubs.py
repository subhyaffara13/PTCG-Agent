import os

def generate_stubs(options: Options) -> None:
    """Main entry point for the program."""
    mypy_opts = mypy_options(options)
    py_modules, pyc_modules, c_modules = collect_build_targets(options, mypy_opts)
    all_modules = py_modules + pyc_modules + c_modules
    all_module_names = sorted(m.module for m in all_modules)
    # Use parsed sources to generate stubs for Python modules.
    generate_asts_for_modules(py_modules, options.parse_only, mypy_opts, options.verbose)
    files = []
    for mod in py_modules + pyc_modules:
        assert mod.path is not None, "Not found module was not skipped"
        target = mod.module.replace(".", "/")
        if os.path.basename(mod.path) in ["__init__.py", "__init__.pyc"]:
            target += "/__init__.pyi"
        else:
            target += ".pyi"
        target = os.path.join(options.output_dir, target)
        files.append(target)
        with generate_guarded(mod.module, target, options.ignore_errors, options.verbose):
            generate_stub_for_py_module(
                mod,
                target,
                parse_only=options.parse_only,
                inspect=options.inspect or mod in pyc_modules,
                include_private=options.include_private,
                export_less=options.export_less,
                include_docstrings=options.include_docstrings,
                doc_dir=options.doc_dir,
                all_modules=all_module_names,
            )

    # Separately analyse C modules using different logic.
    for mod in c_modules:
        if any(py_mod.module.startswith(mod.module + ".") for py_mod in all_modules):
            target = mod.module.replace(".", "/") + "/__init__.pyi"
        else:
            target = mod.module.replace(".", "/") + ".pyi"
        target = os.path.join(options.output_dir, target)
        files.append(target)
        with generate_guarded(mod.module, target, options.ignore_errors, options.verbose):
            generate_stub_for_c_module(
                mod.module,
                target,
                known_modules=all_module_names,
                doc_dir=options.doc_dir,
                include_private=options.include_private,
                export_less=options.export_less,
                include_docstrings=options.include_docstrings,
            )
    num_modules = len(all_modules)
    if not options.quiet and num_modules > 0:
        print("Processed %d modules" % num_modules)
        if len(files) == 1:
            print(f"Generated {files[0]}")
        else:
            print(f"Generated files under {common_dir_prefix(files)}" + os.sep)

