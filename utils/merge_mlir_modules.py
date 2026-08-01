
def merge_mlir_modules(dst_module: ir.Module,
                       sym_name: str,
                       src_module: ir.Module,
                       dst_symtab: ir.SymbolTable | None = None) -> str:
  """
  Args:
    dst_module: the module into which the contents of src_module should be
      moved. Nothing in dst_module will be renamed.
    sym_name: the desired name for the "main" function of src_module after
      merging. This is a hint: the true name may be different because of symbol
      uniquification, and the true name is returned by this function.
    src_module: the module whose contents are to be alpha-renamed, set to
      private visibility, and merged into dst_module. src_module must contain
      exactly one symbol named "main".
    dst_symtab: the symbol table of `dst_module`

      Functions in src_module will be renamed such that they do not collide with
      functions in dst_module.

      This function mutates `src_module`. On return, `src_module` is left in an
      undefined state.

  Returns:
    the name of src_module's main() function, after renaming.
  """
  assert dst_module.context == src_module.context

  src_symtab = ir.SymbolTable(src_module.operation)
  dst_symtab = dst_symtab or ir.SymbolTable(dst_module.operation)
  used_names = set()

  # Rename all symbols in src_module that clash with names in dst_module, or
  # are the "main" symbol.
  renamings = {}
  for op_view in src_module.body.operations:
    op = type_cast(func_dialect.FuncOp, op_view)
    name = op.sym_name.value
    should_rename = name in dst_symtab or name == "main"
    if should_rename:
      base_name = sym_name if name == "main" else name
      new_name = base_name
      i = 0
      # Replacements are chosen such that the new names are present in neither
      # src_module, dst_module, or the set of fresh names we've already used.
      # Since we rename names one at a time, if new names were in src_module,
      # they might themselves collide with a later renaming.
      while (new_name in src_symtab or new_name in dst_symtab or
             new_name in used_names):
        new_name = f"{base_name}_{i}"
        i += 1
      renamings[name] = new_name
      used_names.add(new_name)

  # Apply the symbol renamings to symbol definitions.
  private = ir.StringAttr.get("private")
  for op_view in src_module.body.operations:
    op = type_cast(func_dialect.FuncOp, op_view)
    name = op.sym_name.value
    if name in renamings:
      src_symtab.set_symbol_name(op, renamings[name])
    op.attributes["sym_visibility"] = private

  # Apply the symbol renamings to symbol uses.
  for old_name, new_name in renamings.items():
    for op in src_module.body.operations:
      src_symtab.replace_all_symbol_uses(old_name, new_name, op)

  for op in src_module.body.operations:
    dst_module.body.append(op)
    dst_symtab.insert(op)

  return renamings["main"]

