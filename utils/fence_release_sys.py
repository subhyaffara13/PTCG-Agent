
def fence_release_sys():
  llvm.inline_asm(
      ir.Type.parse("!llvm.void"),
      [],
      "fence.release.sys;",
      "",
      has_side_effects=True,
  )

