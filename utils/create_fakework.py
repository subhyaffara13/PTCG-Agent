
def create_fakework(args, return_first_arg=True):  # type: ignore[no-untyped-def]
    work = FakeWork()
    work.seq_id = generate_unique_id()
    fakework_script_obj = work.boxed()
    return (args[0], fakework_script_obj) if return_first_arg else fakework_script_obj

