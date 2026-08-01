
def ret_work(ret):
    fut = Future()
    fut.set_result(ret)
    return _create_work_from_future(fut)

