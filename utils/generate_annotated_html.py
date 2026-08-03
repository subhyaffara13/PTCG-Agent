import os
import sys

def generate_annotated_html(
    html_fnam: str, result: BuildResult, modules: dict[str, ModuleIR], mapper: Mapper
) -> None:
    annotations = []
    for mod, mod_ir in modules.items():
        path = result.graph[mod].path
        tree = result.graph[mod].tree
        assert tree is not None
        annotations.append(
            generate_annotations(path or "<source>", tree, mod_ir, result.types, mapper)
        )
    html = generate_html_report(annotations)
    with open(html_fnam, "w") as f:
        f.write(html)

    formatter = FancyFormatter(sys.stdout, sys.stderr, False)
    formatted = formatter.style(os.path.abspath(html_fnam), "none", underline=True, bold=True)
    print(f"\nWrote {formatted} -- open in browser to view\n")

