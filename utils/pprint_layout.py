
def pprint_layout(v: fa.FragmentedArray | tcgen05.TMEMRef) -> str:
  if isinstance(v, fa.FragmentedArray):
    match v.layout:
      case fa.WGMMA_LAYOUT:
        return "WGMMA"
      case fa.WGMMA_ROW_LAYOUT:
        return "WGMMA_ROW"
      case fa.WGMMA_TRANSPOSED_LAYOUT:
        return "WGMMA_TRANSPOSED"
      case fa.TCGEN05_LAYOUT:
        return "TCGEN05"
      case fa.TCGEN05_TRANSPOSED_LAYOUT:
        return "TCGEN05_TRANSPOSED"
      case fa.TMEM_NATIVE_LAYOUT:
        return "TCGEN05_TMEM_NATIVE"
      case _:
        return str(v.layout)
  else:
    assert isinstance(v, tcgen05.TMEMRef), v
    if v.layout == tcgen05.tmem_default_layout(packing=v.packing):
      return f"TMEM_DEFAULT(packing={v.packing})"
    return str(v.layout)

