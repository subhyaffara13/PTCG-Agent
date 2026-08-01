
def canonic_package_data(package_data: dict) -> dict:
    if "*" in package_data:
        package_data[""] = package_data.pop("*")
    return package_data

