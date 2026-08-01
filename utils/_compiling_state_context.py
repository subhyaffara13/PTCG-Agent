
def _compiling_state_context():
    old_compiling_flag = torch.compiler._is_compiling_flag
    old_exporting_flag = torch.compiler._is_exporting_flag
    try:
        torch.compiler._is_compiling_flag = True
        torch.compiler._is_exporting_flag = True
        yield
    finally:
        torch.compiler._is_compiling_flag = old_compiling_flag
        torch.compiler._is_exporting_flag = old_exporting_flag

