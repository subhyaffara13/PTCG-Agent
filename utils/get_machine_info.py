
def get_machine_info(silent=True) -> str:
    machine = MachineInfo(silent)
    return json.dumps(machine.machine_info, indent=2)

