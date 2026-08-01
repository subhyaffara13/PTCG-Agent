
def _patch_setuptools_copy_extensions_to_source() -> None:
    """Skip redundant `.so` copies for extensions we generated.

    setuptools' copy_extensions_to_source rewrites every `.so` in the
    source tree on every build_ext, even when nothing changed. On macOS
    this invalidates AMFI's signature cache (~100 ms re-verification per
    `.so` on the next import), eating most of the separate=True
    incremental speedup.

    The patch is global because copy_extensions_to_source runs during
    setup()'s build_ext command, after mypycify() has already returned;
    we can't scope a context manager around it. Instead the skip only
    fires for extensions tagged by mypycify (via the marker attribute),
    so other setuptools users in the same setup.py see the unmodified
    upstream behavior, including stub writes.
    """
    global _setuptools_patch_applied
    if _setuptools_patch_applied:
        return
    _setuptools_patch_applied = True

    from setuptools.command.build_ext import build_ext as _build_ext

    original = _build_ext.copy_extensions_to_source

    def _files_match(a: str, b: str) -> bool:
        try:
            sa = os.stat(a)
            sb = os.stat(b)
        except OSError:
            return False
        # Compare size + whole-second mtime. distutils' copy_file
        # propagates the source mtime, but macOS drops sub-second
        # precision on write so the float values never match verbatim.
        return sa.st_size == sb.st_size and int(sa.st_mtime) == int(sb.st_mtime)

    def patched(self: Any) -> None:
        build_py = self.get_finalized_command("build_py")

        def is_redundant(ext: Any) -> bool:
            if not getattr(ext, _MYPYC_EXTENSION_MARKER, False):
                return False
            inplace_file, regular_file = self._get_inplace_equivalent(build_py, ext)
            return _files_match(regular_file, inplace_file)

        # Hide our already-fresh extensions from setuptools' loop and
        # let it handle whatever's left. Delegating instead of
        # reimplementing the body means future setuptools changes carry
        # over for free. self.extensions is restored before we return
        # so anything that inspects it later sees the original list.
        saved = self.extensions
        self.extensions = [ext for ext in saved if not is_redundant(ext)]
        try:
            original(self)
        finally:
            self.extensions = saved

    _build_ext.copy_extensions_to_source = patched  # type: ignore[method-assign]

