
def find_module_and_diagnose(
    manager: BuildManager,
    id: str,
    options: Options,
    caller_state: State | None = None,
    caller_line: int = 0,
    ancestor_for: State | None = None,
    root_source: bool = False,
    skip_diagnose: bool = False,
) -> tuple[str, str]:
    """Find a module by name, respecting follow_imports and producing diagnostics.

    If the module is not found, then the ModuleNotFound exception is raised.

    Args:
      id: module to find
      options: the options for the module being loaded
      caller_state: the state of the importing module, if applicable
      caller_line: the line number of the import
      ancestor_for: the child module this is an ancestor of, if applicable
      root_source: whether this source was specified on the command line
      skip_diagnose: skip any error diagnosis and reporting (but ModuleNotFound is
          still raised if the module is missing)

    The specified value of follow_imports for a module can be overridden
    if the module is specified on the command line or if it is a stub,
    so we compute and return the "effective" follow_imports of the module.

    Returns a tuple containing (file path, target's effective follow_imports setting)
    """
    result = find_module_with_reason(id, manager)
    if isinstance(result, str):
        # For non-stubs, look at options.follow_imports:
        # - normal (default) -> fully analyze
        # - silent -> analyze but silence errors
        # - skip -> don't analyze, make the type Any
        follow_imports = options.follow_imports
        if (
            root_source  # Honor top-level modules
            or (
                result.endswith(".pyi")  # Stubs are always normal
                and not options.follow_imports_for_stubs  # except when they aren't
            )
            or id in CORE_BUILTIN_MODULES  # core is always normal
        ):
            follow_imports = "normal"
        if skip_diagnose:
            pass
        elif follow_imports == "silent":
            # Still import it, but silence non-blocker errors.
            manager.log(f"Silencing {result} ({id})")
        elif follow_imports == "skip" or follow_imports == "error":
            # In 'error' mode, produce special error messages.
            if id not in manager.missing_modules:
                manager.log(f"Skipping {result} ({id})")
            if follow_imports == "error":
                if ancestor_for:
                    skipping_ancestor(manager, id, result, ancestor_for)
                else:
                    skipping_module(manager, caller_line, caller_state, id, result)
            reason = SuppressionReason.SKIPPED
            if options.ignore_missing_imports:
                # Performance optimization: when we are ignoring imports, there is no
                # difference for the caller between skipped import and actually missing one.
                reason = SuppressionReason.NOT_FOUND
            raise ModuleNotFound(reason=reason)
        if is_silent_import_module(manager, result) and not root_source:
            follow_imports = "silent"
        return result, follow_imports
    else:
        # Could not find a module.  Typically, the reason is a
        # misspelled module name, missing stub, module not in
        # search path or the module has not been installed.

        ignore_missing_imports = options.ignore_missing_imports

        if skip_diagnose:
            raise ModuleNotFound
        if caller_state:
            if not (ignore_missing_imports or in_partial_package(id, manager)):
                module_not_found(manager, caller_line, caller_state, id, result)
            raise ModuleNotFound
        elif root_source:
            # If we can't find a root source it's always fatal.
            # TODO: This might hide non-fatal errors from
            # root sources processed earlier.
            raise CompileError([f'mypy: error: Cannot find module "{id}"'])
        else:
            raise ModuleNotFound

