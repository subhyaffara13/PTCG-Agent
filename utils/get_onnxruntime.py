
def get_onnxruntime():
    version = "1.16.3"
    base_dir = os.path.abspath(os.path.dirname(__file__))
    
    if sys.platform == "win32":
        ort_dir = os.path.join(base_dir, f"onnxruntime-win-x64-{version}")
        url = f"https://github.com/microsoft/onnxruntime/releases/download/v{version}/onnxruntime-win-x64-{version}.zip"
        archive_path = os.path.join(base_dir, f"onnxruntime-win-x64-{version}.zip")
    else:
        ort_dir = os.path.join(base_dir, f"onnxruntime-linux-x64-{version}")
        url = f"https://github.com/microsoft/onnxruntime/releases/download/v{version}/onnxruntime-linux-x64-{version}.tgz"
        archive_path = os.path.join(base_dir, f"onnxruntime-linux-x64-{version}.tgz")
        
    if os.path.exists(ort_dir):
        return ort_dir

    if not os.path.exists(archive_path):
        print(f"Downloading ONNX Runtime from {url}...")
        urllib.request.urlretrieve(url, archive_path)
        print("Download complete.")

    print(f"Extracting {archive_path}...")
    if sys.platform == "win32":
        with zipfile.ZipFile(archive_path, 'r') as zip_ref:
            zip_ref.extractall(base_dir)
    else:
        with tarfile.open(archive_path, 'r:gz') as tar_ref:
            tar_ref.extractall(base_dir)

    print("Extraction complete.")
    return ort_dir


def get_onnxruntime():
    version = "1.16.3"
    base_dir = os.path.abspath(os.path.dirname(__file__))
    
    if sys.platform == "win32":
        ort_dir = os.path.join(base_dir, f"onnxruntime-win-x64-{version}")
        url = f"https://github.com/microsoft/onnxruntime/releases/download/v{version}/onnxruntime-win-x64-{version}.zip"
        archive_path = os.path.join(base_dir, f"onnxruntime-win-x64-{version}.zip")
    else:
        ort_dir = os.path.join(base_dir, f"onnxruntime-linux-x64-{version}")
        url = f"https://github.com/microsoft/onnxruntime/releases/download/v{version}/onnxruntime-linux-x64-{version}.tgz"
        archive_path = os.path.join(base_dir, f"onnxruntime-linux-x64-{version}.tgz")
        
    if os.path.exists(ort_dir):
        return ort_dir

    if not os.path.exists(archive_path):
        print(f"Downloading ONNX Runtime from {url}...")
        urllib.request.urlretrieve(url, archive_path)
        print("Download complete.")

    print(f"Extracting {archive_path}...")
    if sys.platform == "win32":
        with zipfile.ZipFile(archive_path, 'r') as zip_ref:
            zip_ref.extractall(base_dir)
    else:
        with tarfile.open(archive_path, 'r:gz') as tar_ref:
            tar_ref.extractall(base_dir)

    print("Extraction complete.")
    return ort_dir

