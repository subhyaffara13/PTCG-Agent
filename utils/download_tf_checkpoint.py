import os

def download_tf_checkpoint(model_name, tf_models_dir="tf_models"):
    import pathlib  # noqa: PLC0415

    base_dir = os.path.join(pathlib.Path(__file__).parent.absolute(), tf_models_dir)
    ckpt_dir = os.path.join(base_dir, model_name)

    if not os.path.exists(ckpt_dir):
        os.makedirs(ckpt_dir)

    tf_ckpt_url = TFMODELS[model_name][3]

    import re  # noqa: PLC0415

    if re.search(".zip$", tf_ckpt_url) is not None:
        zip_dir = download_compressed_file(tf_ckpt_url, ckpt_dir)

        # unzip file
        import zipfile  # noqa: PLC0415

        with zipfile.ZipFile(zip_dir, "r") as zip_ref:
            zip_ref.extractall(ckpt_dir)
            os.remove(zip_dir)

        return get_ckpt_prefix_path(ckpt_dir)

    elif re.search(".tar.gz$", tf_ckpt_url) is not None:
        tar_dir = download_compressed_file(tf_ckpt_url, ckpt_dir)

        # untar file
        import tarfile  # noqa: PLC0415

        with tarfile.open(tar_dir, "r") as tar_ref:
            tar_ref.extractall(ckpt_dir)
            os.remove(tar_dir)

        return get_ckpt_prefix_path(ckpt_dir)

    else:
        for filename in [
            "checkpoint",
            "model.ckpt.data-00000-of-00001",
            "model.ckpt.index",
            "model.ckpt.meta",
        ]:
            r = requests.get(tf_ckpt_url + "/" + filename)
            with open(os.path.join(ckpt_dir, filename), "wb") as f:
                f.write(r.content)

        return get_ckpt_prefix_path(ckpt_dir)

