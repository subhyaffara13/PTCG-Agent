
def build_helper(source: str) -> build.BuildResult:
    return build.build(
        sources=[BuildSource("main.pyi", None, textwrap.dedent(source))],
        options=Options(),
        alt_lib_path=test_temp_dir,
    )

