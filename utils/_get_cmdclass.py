import os

def _get_cmdclass(pkg_source_path):
  from setuptools.command.build_py import build_py as build_py_orig  # pyrefly: ignore[missing-source-for-stubs]
  from setuptools.command.sdist import sdist as sdist_orig  # pyrefly: ignore[missing-source-for-stubs]

  class _build_py(build_py_orig):
    def run(self):
      if _release_version is None:
        this_file_in_build_dir = os.path.join(
          self.build_lib,
          pkg_source_path,
          os.path.basename(__file__))
        # super().run() only copies files from source -> build if they are
        # missing or outdated. Because _write_version(...) modifies the copy of
        # this file in the build tree, re-building from the same JAX directory
        # would not automatically re-copy a clean version, and _write_version
        # would fail without this deletion. See jax-ml/jax#18252.
        if os.path.isfile(this_file_in_build_dir):
          os.unlink(this_file_in_build_dir)
      else:
        this_file_in_build_dir = ""
      super().run()
      if this_file_in_build_dir:
        _write_version(this_file_in_build_dir)

  class _sdist(sdist_orig):
    def make_release_tree(self, base_dir, files):
      super().make_release_tree(base_dir, files)
      if _release_version is None:
        _write_version(os.path.join(base_dir, pkg_source_path,
                                    os.path.basename(__file__)))

  return dict(sdist=_sdist, build_py=_build_py)


def _get_cmdclass(pkg_source_path):
  from setuptools.command.build_py import build_py as build_py_orig  # pyrefly: ignore[missing-source-for-stubs]
  from setuptools.command.sdist import sdist as sdist_orig  # pyrefly: ignore[missing-source-for-stubs]

  class _build_py(build_py_orig):
    def run(self):
      if _release_version is None:
        this_file_in_build_dir = os.path.join(
          self.build_lib,
          pkg_source_path,
          os.path.basename(__file__))
        # super().run() only copies files from source -> build if they are
        # missing or outdated. Because _write_version(...) modifies the copy of
        # this file in the build tree, re-building from the same JAX directory
        # would not automatically re-copy a clean version, and _write_version
        # would fail without this deletion. See jax-ml/jax#18252.
        if os.path.isfile(this_file_in_build_dir):
          os.unlink(this_file_in_build_dir)
      else:
        this_file_in_build_dir = ""
      super().run()
      if this_file_in_build_dir:
        _write_version(this_file_in_build_dir)

  class _sdist(sdist_orig):
    def make_release_tree(self, base_dir, files):
      super().make_release_tree(base_dir, files)
      if _release_version is None:
        _write_version(os.path.join(base_dir, pkg_source_path,
                                    os.path.basename(__file__)))

  return dict(sdist=_sdist, build_py=_build_py)

