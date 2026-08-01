
def convert_dos_path(s):
    r"""Convert paths using native DOS format like:
        "\Device\HarddiskVolume1\Windows\systemew\file.txt" or
        "\??\C:\Windows\systemew\file.txt"
    into:
        "C:\Windows\systemew\file.txt".
    """
    if s.startswith('\\\\'):
        return s
    rawdrive = '\\'.join(s.split('\\')[:3])
    if rawdrive in {"\\??\\UNC", "\\Device\\Mup"}:
        rawdrive = '\\'.join(s.split('\\')[:5])
        driveletter = '\\\\' + '\\'.join(s.split('\\')[3:5])
    elif rawdrive.startswith('\\??\\'):
        driveletter = s.split('\\')[2]
    else:
        driveletter = cext.QueryDosDevice(rawdrive)
    remainder = s[len(rawdrive) :]
    return os.path.join(driveletter, remainder)

