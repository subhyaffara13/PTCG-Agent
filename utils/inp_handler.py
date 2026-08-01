
def inp_handler(name):
    from pynput.keyboard import Controller as KeyboardController
    from pynput.keyboard import Key

    keyboard = KeyboardController()
    time.sleep(0.1)
    choices = ["w", "a", "s", "d", "j", "k", Key.left, Key.right, Key.up, Key.down]
    NUM_TESTS = 50
    for x in range(NUM_TESTS):
        i = random.choice(choices) if x != NUM_TESTS - 1 else Key.esc
        keyboard.press(i)
        time.sleep(0.1)
        keyboard.release(i)

