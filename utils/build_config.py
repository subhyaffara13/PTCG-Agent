from typing import Any

def build_config(
    checkpoint_path: str, axis_size: int, strategy: str = "fsdp"
) -> dict[str, dict[str, Any]]:
  """Builds the per-leaf sharding map for every leaf in the checkpoint.

  Args:
    checkpoint_path: Path (local or `gs://`) to an Orbax checkpoint dir.
    axis_size: Size of the single mesh axis to shard along.
    strategy: Sharding strategy, "fsdp" or "tp_inner".

  Returns:
    A `{leaf_name: entry}` sharding-config map.

  Raises:
    ValueError: If `strategy` is unknown.
  """
  try:
    axis_name, spec_fn = _STRATEGIES[strategy]
  except KeyError as e:
    raise ValueError(
        f"Unknown strategy {strategy!r}; supported: "
        + ", ".join(sorted(_STRATEGIES))
    ) from e
  metadata = ocp.metadata(epath.Path(checkpoint_path))
  flat = tree_utils.to_flat_dict(metadata.metadata, sep=".")
  mesh = {"shape": [axis_size], "axes": [axis_name]}
  out: dict[str, dict[str, Any]] = {}
  for name, leaf in flat.items():
    shape = list(leaf.shape)
    out[name] = {
        "shape": shape,
        "dtype": np.dtype(leaf.dtype).name,
        "sharding": {
            "mesh": mesh,
            "spec": spec_fn(shape, axis_name, axis_size),
        },
    }
  return out


def build_config() -> dict[str, str]:
    """
    Return a dictionary containing build configuration settings.

    All dictionary keys and values are strings, for example ``False`` is
    returned as ``"False"``.

        .. versionadded:: 1.1.0
    """
    return dict(
        # Python settings
        python_version="3.12",
        python_install_dir=r"c:/Lib/site-packages/",
        python_path=r"C:/Users/runneradmin/AppData/Local/Temp/build-env-u5bybl2l/Scripts/python.exe",

        # Package versions
        contourpy_version="1.3.3",
        meson_version="1.8.2",
        mesonpy_version="0.18.0",
        pybind11_version="3.0.0",

        # Misc meson settings
        meson_backend="ninja",
        build_dir=r"D:/a/contourpy/contourpy/.mesonpy-esbcvpny/lib/contourpy/util",
        source_dir=r"D:/a/contourpy/contourpy/lib/contourpy/util",
        cross_build="False",

        # Build options
        build_options=r"-Dbuildtype=release -Db_ndebug=if-release -Db_vscrt=mt '-Dcpp_link_args=['ucrt.lib','vcruntime.lib','/nodefaultlib:libucrt.lib','/nodefaultlib:libvcruntime.lib']' -Dvsenv=True '--native-file=D:/a/contourpy/contourpy/.mesonpy-esbcvpny/meson-python-native-file.ini'",
        buildtype="release",
        cpp_std="c++17",
        debug="False",
        optimization="3",
        vsenv="True",
        b_ndebug="if-release",
        b_vscrt="mt",

        # C++ compiler
        compiler_name="msvc",
        compiler_version="19.44.35213",
        linker_id="link",
        compile_command="cl",

        # Host machine
        host_cpu="x86_64",
        host_cpu_family="x86_64",
        host_cpu_endian="little",
        host_cpu_system="windows",

        # Build machine, same as host machine if not a cross_build
        build_cpu="x86_64",
        build_cpu_family="x86_64",
        build_cpu_endian="little",
        build_cpu_system="windows",
    )

