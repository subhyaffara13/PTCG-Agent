import json

def get_windows_version(run_lambda):
    ret = run_and_read_all(
        run_lambda,
        'powershell.exe "gwmi -Class Win32_OperatingSystem | Select-Object -Property Caption,\
        OSArchitecture,Version | ConvertTo-Json"',
    )
    try:
        obj = json.loads(ret)
        ret = f'{obj["Caption"]} ({obj["Version"]} {obj["OSArchitecture"]})'
    except ValueError as e:
        ret += f"\n{str(e)}"
    return ret

