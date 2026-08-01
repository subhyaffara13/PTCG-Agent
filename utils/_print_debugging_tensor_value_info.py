
def _print_debugging_tensor_value_info(msg, arg):
    # helper for printing debugging stats for intermediate tensor values
    # at jit inductor level codegen
    max_numel_to_print = 64
    print(msg)
    if not isinstance(arg, torch.Tensor):
        print("Value: ", arg)
        return
    numel = arg.float().numel()
    # print the debug printing stats
    if numel <= max_numel_to_print:
        print(arg)
    print("Number of elements: ", numel)
    print("Size: ", arg.float().size())
    print("Dtype: ", arg.float().mean().item())
    print("Mean: ", arg.float().mean().item())
    print("Min: ", arg.float().min().item())
    print("Max: ", arg.float().max().item())
    print("Std: ", arg.float().std().item())

