
def get_wheel_members(wheel_path):
    with ZipFile(wheel_path) as zipfile:
        return set(zipfile.namelist())

