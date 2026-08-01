
def play_file(filename):
    """
    This function will call add_file and play it if successful
    The music will fade in during the first 4 seconds
    set_endevent is used to post a MUSIC_DONE event when the song finishes
    The main loop will call play_next() when the MUSIC_DONE event is received
    """
    global starting_pos

    if add_file(filename):
        try:  # we must do this in case the file is not a valid audio file
            pg.mixer.music.load(music_file_list[-1])
        except pg.error as e:
            print(e)  # print description such as 'Not an Ogg Vorbis audio stream'
            if filename in music_file_list:
                music_file_list.remove(filename)
                print(f"{filename} removed from file list")
            return
        pg.mixer.music.play(fade_ms=4000)
        pg.mixer.music.set_volume(volume)

        if filename.rpartition(".")[2].lower() in music_can_seek:
            print("file supports seeking")
            starting_pos = 0
        else:
            print("file does not support seeking")
            starting_pos = -1
        pg.mixer.music.set_endevent(MUSIC_DONE)

