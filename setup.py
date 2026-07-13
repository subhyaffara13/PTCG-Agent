import os
import sys
import shutil
import urllib.request
import zipfile
import tarfile
from setuptools import setup
from setuptools.command.build_ext import build_ext as _build_ext

from pybind11.setup_helpers import Pybind11Extension, build_ext

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

ort_dir = get_onnxruntime()

class BuildExt(build_ext):
    def run(self):
        super().run()
        for ext in self.extensions:
            ext_path = self.get_ext_fullpath(ext.name)
            ext_dir = os.path.dirname(ext_path)
            
            if sys.platform == "win32":
                src_dll = os.path.join(ort_dir, "lib", "onnxruntime.dll")
                dst_dll = os.path.join(ext_dir, "onnxruntime.dll")
                if os.path.exists(src_dll):
                    shutil.copy2(src_dll, dst_dll)
                    shutil.copy2(src_dll, os.path.join(os.path.abspath(os.path.dirname(__file__)), "onnxruntime.dll"))
            else:
                src_so = os.path.join(ort_dir, "lib", "libonnxruntime.so.1.16.3")
                if not os.path.exists(src_so):
                    src_so = os.path.join(ort_dir, "lib", "libonnxruntime.so")
                dst_so = os.path.join(ext_dir, "libonnxruntime.so")
                if os.path.exists(src_so):
                    shutil.copy2(src_so, dst_so)
                    shutil.copy2(src_so, os.path.join(os.path.abspath(os.path.dirname(__file__)), "libonnxruntime.so"))

ext_modules = [
    Pybind11Extension(
        "ptcg_core",
        [
            "src/bindings.cpp",
            "src/ptcg_simulator.cpp",
            "src/cpp_mcts.cpp",
        ],
        cxx_std=17,
        include_dirs=[
            "src",
            os.path.join(ort_dir, "include"),
        ],
        library_dirs=[
            os.path.join(ort_dir, "lib"),
        ],
        libraries=["onnxruntime"],
    ),
]

setup(
    name="ptcg_core",
    version="1.0.0",
    author="TCG Expert",
    description="High-performance Pokemon TCG simulator and MCTS engine in C++",
    ext_modules=ext_modules,
    cmdclass={"build_ext": BuildExt},
    zip_safe=False,
    python_requires=">=3.7",
)

