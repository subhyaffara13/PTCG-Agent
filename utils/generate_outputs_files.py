
def generate_outputs_files(model_path, dummy_inputs, outputs_path, use_gpu):
    dir_path = Path(outputs_path)
    if dir_path.exists() and dir_path.is_dir():
        import shutil  # noqa: PLC0415

        shutil.rmtree(outputs_path)
    dir_path.mkdir(parents=True, exist_ok=True)

    process = multiprocessing.Process(target=inference, args=(model_path, dummy_inputs, outputs_path, use_gpu))
    process.start()
    process.join()

