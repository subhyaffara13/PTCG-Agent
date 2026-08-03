import os

def _append_to_datas(file_path):
    res_path = os.path.join(pygame_folder, file_path)
    if os.path.exists(res_path):
        datas.append((res_path, "pygame"))

