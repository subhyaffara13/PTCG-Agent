
def manual_control_test(manual_control):
    manual_in_thread = threading.Thread(target=inp_handler, args=(1,))

    manual_in_thread.start()

    try:
        manual_control()
    except Exception as e:
        raise Exception("manual_control() has crashed. Please fix it.") from e

    manual_in_thread.join()

