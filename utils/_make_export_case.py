
def _make_export_case(m, name, configs):
    if not isinstance(m, torch.nn.Module):
        raise TypeError("Export case class should be a torch.nn.Module.")

    if "description" not in configs:
        # Fallback to docstring if description is missing.
        if m.__doc__ is None:
            raise AssertionError(
                f"Could not find description or docstring for export case: {m}"
            )
        configs = {**configs, "description": m.__doc__}
    # pyrefly: ignore [bad-argument-type]
    return ExportCase(**{**configs, "model": m, "name": name})

