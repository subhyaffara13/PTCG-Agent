
def maybe_fbcode_instructions() -> str:
    if is_fbcode():
        extra_deps_formatted = "\n".join([f'        "{dep}",' for dep in extra_deps])
        if len(extra_deps_formatted) > 0:
            extra_deps_formatted = "\n" + extra_deps_formatted
        return f"""\
\"\"\"
To run this script in fbcode:
- Create a directory (//scripts/{{your_unixname}}/repro)
- Put this file in scripts/{{your_unixname}}/repro/fx_graph_runnable.py
- Add a TARGETS file that looks like the following
- `buck2 run //scripts/{{your_unixname}}/repro:repro`

NOTE: you may need additional deps to actually be able to run the script.
```
# Contents of TARGETS file
load("@fbcode_macros//build_defs:python_binary.bzl", "python_binary")

python_binary(
    name = "repro",
    main_src = "fx_graph_runnable.py",
    deps = [
        "//caffe2:torch",{extra_deps_formatted}
    ],
)
```
\"\"\"
"""
    else:
        return ""

