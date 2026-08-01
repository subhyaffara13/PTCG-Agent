
def is_free_variable(builder: IRBuilder, symbol: SymbolNode) -> bool:
    fitem = builder.fn_info.fitem
    return fitem in builder.free_variables and symbol in builder.free_variables[fitem]

