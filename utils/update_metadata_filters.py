
def update_metadata_filters(metadata, jupyter_md, cell_metadata):
    """Update or set the notebook and cell metadata filters"""

    if not jupyter_md:
        # Set a metadata filter equal to the current metadata in script
        metadata.setdefault("jupytext", {})["notebook_metadata_filter"] = "-all"
        metadata["jupytext"].setdefault(
            "cell_metadata_filter",
            metadata_filter_as_string({"additional": cell_metadata, "excluded": "all"}),
        )
    elif "cell_metadata_filter" in metadata.get("jupytext", {}):
        # Update the existing metadata filter
        metadata_filter = metadata_filter_as_dict(metadata.get("jupytext", {})["cell_metadata_filter"])
        if isinstance(metadata_filter.get("excluded"), list):
            metadata_filter["excluded"] = [key for key in metadata_filter["excluded"] if key not in cell_metadata]
        metadata_filter.setdefault("additional", [])
        if isinstance(metadata_filter.get("additional"), list):
            for key in cell_metadata:
                if key not in metadata_filter["additional"]:
                    metadata_filter["additional"].append(key)
        metadata.setdefault("jupytext", {})["cell_metadata_filter"] = metadata_filter_as_string(metadata_filter)
    else:
        # Update the notebook metadata filter to include existing entries 376
        nb_md_filter = metadata.get("jupytext", {}).get("notebook_metadata_filter", "").split(",")
        nb_md_filter = [key for key in nb_md_filter if key]
        if "all" in nb_md_filter or "-all" in nb_md_filter:
            return
        for key in metadata:
            if key in _DEFAULT_NOTEBOOK_METADATA.split(",") or key in nb_md_filter or ("-" + key) in nb_md_filter:
                continue
            nb_md_filter.append(key)
        if nb_md_filter:
            metadata.setdefault("jupytext", {})["notebook_metadata_filter"] = ",".join(nb_md_filter)

