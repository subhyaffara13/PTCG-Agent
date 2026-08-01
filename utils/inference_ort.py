
def inference_ort(ort_session, ort_inputs, result_template, repeat_times, batch_size, warm_up_repeat=0):
    result = {}
    timeit.repeat(lambda: ort_session.run(None, ort_inputs), number=1, repeat=warm_up_repeat)  # Dry run
    latency_list = timeit.repeat(lambda: ort_session.run(None, ort_inputs), number=1, repeat=repeat_times)
    result.update(result_template)
    result.update({"io_binding": False})
    result.update(get_latency_result(latency_list, batch_size))
    return result

