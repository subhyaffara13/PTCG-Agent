
def cexpr_index(index):
    return f"static_cast<{INDEX_TYPE}>({cexpr(index)})"

