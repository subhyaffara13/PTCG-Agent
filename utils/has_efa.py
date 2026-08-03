import subprocess

def has_efa() -> bool:
    """
    If shell command `fi_info -p efa -t FI_EP_RDM` returns exit code 0 then we assume that the machine has
    Libfabric EFA interfaces and EFA software components installed,
    see https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/efa-start.html.
    """

    try:
        return (
            subprocess.run(
                ["fi_info", "-p", "efa", "-t", "FI_EP_RDM"], check=False
            ).returncode
            == 0
        )
    except FileNotFoundError:
        pass
    return False

