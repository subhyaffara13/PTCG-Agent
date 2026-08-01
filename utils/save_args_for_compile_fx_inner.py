
def save_args_for_compile_fx_inner(*args: Any, **kwargs: Any) -> None:
    """
    This function is used to save arguments for a compile_fx_inner function call
    to the file system.  Later on one can replay the compile_fx_inner call
    with the saved arguments using load_args_and_run_compile_fx_inner.
    """

    folder = os.path.join(tempfile.gettempdir(), "inductor_saved_args")
    if not os.path.exists(folder):
        os.mkdir(folder)

    def handle_tensor(x: Any) -> Any:
        """
        Pickle FakeTensor will result in error:
        AttributeError: Can't pickle local object 'WeakValueDictionary.__init__.<locals>.remove'

        Convert all Tensor to metadata. This may also makes pickle faster.
        """
        if isinstance(x, torch.Tensor):
            return TensorMetadataHolder(_extract_tensor_metadata(x), x.device)
        else:
            return x

    args_to_save, kwargs_to_save = tree_map(handle_tensor, (args, kwargs))

    fn_name = "compile_fx_inner"
    path = f"{folder}/{fn_name}_{next(save_args_cnt)}.pkl"
    with open(path, "wb") as f:
        pickle.dump((args_to_save, kwargs_to_save), f)

    if log.isEnabledFor(logging.DEBUG):
        message = f"""
Arguments for a compile_fx_inner call is saved to {path}. To replay the call,
run the following:

from torch._inductor.debug import load_args_and_run_compile_fx_inner
load_args_and_run_compile_fx_inner({path!r})
        """
        # call print rather than log.debug. log.debug will print message
        # prefix for each line which makes the code snippet harder to be
        # copied.
        # Not a big deal since the code is already been guarded by checking
        # the log level.
        print(message)

