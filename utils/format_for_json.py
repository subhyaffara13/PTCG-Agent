import json

def format_for_json(packages: _ProcessedDists, options: Values) -> str:
    data = []
    for dist in packages:
        try:
            version = str(dist.version)
        except InvalidVersion:
            version = dist.raw_version
        info = {
            "name": dist.raw_name,
            "version": version,
        }
        if options.verbose >= 1:
            info["location"] = dist.location or ""
            info["installer"] = dist.installer
        if options.outdated:
            info["latest_version"] = str(dist.latest_version)
            info["latest_filetype"] = dist.latest_filetype
        editable_project_location = dist.editable_project_location
        if editable_project_location:
            info["editable_project_location"] = editable_project_location
        data.append(info)
    return json.dumps(data)

