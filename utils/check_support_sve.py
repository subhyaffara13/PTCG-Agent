
def check_support_sve(__cache=[]):
    """
    gh-22982
    """

    if __cache:
        return __cache[0]

    import subprocess
    cmd = 'lscpu'
    try:
        output = subprocess.run(cmd, capture_output=True, text=True)
        result = 'sve' in output.stdout
    except (OSError, subprocess.SubprocessError):
        result = False
    __cache.append(result)
    return __cache[0]

