
def num_available_tpu_chips_and_device_id():
  """Returns the device id and number of TPU chips attached through PCI."""
  num_chips = 0
  tpu_version = None
  for vendor_path in glob.glob('/sys/bus/pci/devices/*/vendor'):
    vendor_id = pathlib.Path(vendor_path).read_text().strip()
    if vendor_id != _GOOGLE_PCI_VENDOR_ID:
      continue

    device_path = os.path.join(os.path.dirname(vendor_path), 'device')
    device_id = pathlib.Path(device_path).read_text().strip()
    if device_id in _TPU_PCI_DEVICE_IDS:
      tpu_version = _TPU_PCI_DEVICE_IDS[device_id]
      num_chips += 1

  return num_chips, tpu_version

