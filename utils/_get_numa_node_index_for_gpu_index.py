
def _get_numa_node_index_for_gpu_index(*, gpu_index: int) -> int:
    device_properties = torch.cuda.get_device_properties(gpu_index)

    domain = device_properties.pci_domain_id  # type: ignore[attr-defined]
    bus = device_properties.pci_bus_id  # type: ignore[attr-defined]
    device = device_properties.pci_device_id  # type: ignore[attr-defined]

    # Format to sysfs PCI address: "0000:dc:00.0"
    pci_addr = f"{domain:04x}:{bus:02x}:{device:02x}.0"

    pci_numa_node_absolute_path = f"/sys/bus/pci/devices/{pci_addr}/numa_node"
    with open(pci_numa_node_absolute_path) as f:
        # In systems with only one NUMA node, this will
        # often be saved as -1. In those cases, there is obviously
        # at least one numa node, 0, so we use that.
        return max(int(f.read().strip()), 0)

