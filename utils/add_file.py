
def add_file(filename):
    """
    This function will check if filename exists and is a music file
    If it is the file will be added to a list of music files(even if already there)
    Type checking is by the extension of the file, not by its contents
    We can only discover if the file is valid when we mixer.music.load() it later

    It looks in the file directory and its data subdirectory
    """
    if filename.rpartition(".")[2].lower() not in music_file_types:
        print(f"{filename} not added to file list")
        print("only these files types are allowed: ", music_file_types)
        return False
    elif os.path.exists(filename):
        music_file_list.append(filename)
    elif os.path.exists(os.path.join(main_dir, filename)):
        music_file_list.append(os.path.join(main_dir, filename))
    elif os.path.exists(os.path.join(data_dir, filename)):
        music_file_list.append(os.path.join(data_dir, filename))
    else:
        print("file not found")
        return False
    print(f"{filename} added to file list")
    return True

