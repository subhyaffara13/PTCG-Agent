
def infer_ir_build_options_from_test_name(name: str) -> CompilerOptions | None:
    """Look for magic substrings in test case name to set compiler options.

    Return None if the test case should be skipped (always pass).

    Supported naming conventions:

      *_64bit*:
          Run test case only on 64-bit platforms
      *_32bit*:
          Run test caseonly on 32-bit platforms
      *_python3_10* (or for any Python version):
          Use Python 3.10+ C API features (default: lowest supported version)
      *StripAssert*:
          Don't generate code for assert statements
    """
    # If this is specific to some bit width, always pass if platform doesn't match.
    if "_64bit" in name and IS_32_BIT_PLATFORM:
        return None
    if "_32bit" in name and not IS_32_BIT_PLATFORM:
        return None
    options = CompilerOptions(
        strip_asserts="StripAssert" in name, capi_version=(3, 10), strict_traceback_checks=True
    )
    # A suffix like _python3_10 is used to set the target C API version.
    m = re.search(r"_python([0-9]+)_([0-9]+)(_|\b)", name)
    if m:
        version = (int(m.group(1)), int(m.group(2)))
        assert version >= (3, 10), f"Unsupported _python* suffix: {name}"
        options.capi_version = version
        options.python_version = options.capi_version
    elif "_py" in name or "_Python" in name:
        assert False, f"Invalid _py* suffix (should be _pythonX_Y): {name}"
    if has_test_name_tag(name, "experimental"):
        options.experimental_features = True
    return options

