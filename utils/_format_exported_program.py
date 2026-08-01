
def _format_exported_program(exported_program: torch.export.ExportedProgram) -> str:
    # Adapted from https://github.com/pytorch/pytorch/pull/128476
    # to remove colors
    # Even though we can call graph_module.print_readable directly, since the
    # colored option was added only recently, we can't guarantee that the
    # version of PyTorch used by the user has this option. Therefore, we
    # still call str(ExportedProgram)
    text = f"```python\n{_strip_color_from_string(str(exported_program))}\n```\n\n"
    return text

