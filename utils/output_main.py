
def output_main(device_id=None):
    """Execute a musical keyboard example for the Church Organ instrument

    This is a piano keyboard example, with a two octave keyboard, starting at
    note F3. Left mouse down over a key starts a note, left up stops it. The
    notes are also mapped to the computer keyboard keys, assuming an American
    English PC keyboard (sorry everyone else, but I don't know if I can map to
    absolute key position instead of value.) The white keys are on the second
    row, TAB to BACKSLASH, starting with note F3. The black keys map to the top
    row, '1' to BACKSPACE, starting with F#3. 'r' is middle C. Close the
    window or press ESCAPE to quit the program. Key velocity (note
    amplitude) varies vertically on the keyboard image, with minimum velocity
    at the top of a key and maximum velocity at bottom.

    Default Midi output, no device_id given, is to the default output device
    for the computer.

    """

    # A note to new pygamers:
    #
    # All the midi module stuff is in this function. It is unnecessary to
    # understand how the keyboard display works to appreciate how midi
    # messages are sent.

    # The keyboard is drawn by a Keyboard instance. This instance maps Midi
    # notes to musical keyboard keys. A regions surface maps window position
    # to (Midi note, velocity) pairs. A key_mapping dictionary does the same
    # for computer keyboard keys. Midi sound is controlled with direct method
    # calls to a pygame.midi.Output instance.
    #
    # Things to consider when using pygame.midi:
    #
    # 1) Initialize the midi module with a to pygame.midi.init().
    # 2) Create a midi.Output instance for the desired output device port.
    # 3) Select instruments with set_instrument() method calls.
    # 4) Play notes with note_on() and note_off() method calls.
    # 5) Call pygame.midi.Quit() when finished. Though the midi module tries
    #    to ensure that midi is properly shut down, it is best to do it
    #    explicitly. A try/finally statement is the safest way to do this.
    #

    # GRAND_PIANO = 0
    CHURCH_ORGAN = 19

    instrument = CHURCH_ORGAN
    # instrument = GRAND_PIANO
    start_note = 53  # F3 (white key note), start_note != 0
    n_notes = 24  # Two octaves (14 white keys)

    key_mapping = make_key_mapping(
        [
            pg.K_TAB,
            pg.K_1,
            pg.K_q,
            pg.K_2,
            pg.K_w,
            pg.K_3,
            pg.K_e,
            pg.K_r,
            pg.K_5,
            pg.K_t,
            pg.K_6,
            pg.K_y,
            pg.K_u,
            pg.K_8,
            pg.K_i,
            pg.K_9,
            pg.K_o,
            pg.K_0,
            pg.K_p,
            pg.K_LEFTBRACKET,
            pg.K_EQUALS,
            pg.K_RIGHTBRACKET,
            pg.K_BACKSPACE,
            pg.K_BACKSLASH,
        ],
        start_note,
    )

    pg.init()
    pygame.midi.init()

    _print_device_info()

    if device_id is None:
        port = pygame.midi.get_default_output_id()
    else:
        port = device_id

    print(f"using output_id :{port}:")

    midi_out = pygame.midi.Output(port, 0)
    try:
        midi_out.set_instrument(instrument)
        keyboard = Keyboard(start_note, n_notes)

        screen = pg.display.set_mode(keyboard.rect.size)
        screen.fill(BACKGROUNDCOLOR)
        pg.display.flip()

        background = pg.Surface(screen.get_size())
        background.fill(BACKGROUNDCOLOR)
        dirty_rects = []
        keyboard.draw(screen, background, dirty_rects)
        pg.display.update(dirty_rects)

        regions = pg.Surface(screen.get_size())  # initial color (0,0,0)
        keyboard.map_regions(regions)

        pg.event.set_blocked(pg.MOUSEMOTION)
        mouse_note = 0
        on_notes = set()
        while True:
            e = pg.event.wait()
            if e.type == pg.MOUSEBUTTONDOWN:
                mouse_note, velocity, __, __ = regions.get_at(e.pos)
                if mouse_note and mouse_note not in on_notes:
                    keyboard.key_down(mouse_note)
                    midi_out.note_on(mouse_note, velocity)
                    on_notes.add(mouse_note)
                else:
                    mouse_note = 0
            elif e.type == pg.MOUSEBUTTONUP:
                if mouse_note:
                    midi_out.note_off(mouse_note)
                    keyboard.key_up(mouse_note)
                    on_notes.remove(mouse_note)
                    mouse_note = 0
            elif e.type == pg.QUIT:
                break
            elif e.type == pg.KEYDOWN:
                if e.key == pg.K_ESCAPE:
                    break
                try:
                    note, velocity = key_mapping[e.key]
                except KeyError:
                    pass
                else:
                    if note not in on_notes:
                        keyboard.key_down(note)
                        midi_out.note_on(note, velocity)
                        on_notes.add(note)
            elif e.type == pg.KEYUP:
                try:
                    note, __ = key_mapping[e.key]
                except KeyError:
                    pass
                else:
                    if note in on_notes and note != mouse_note:
                        keyboard.key_up(note)
                        midi_out.note_off(note, 0)
                        on_notes.remove(note)

            dirty_rects = []
            keyboard.draw(screen, background, dirty_rects)
            pg.display.update(dirty_rects)
    finally:
        del midi_out
        pygame.midi.quit()

