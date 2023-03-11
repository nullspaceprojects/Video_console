# NULLSPACEPROJECTS
# RaspberryPi Pico RP2040 Magic Box Keyboard

import time
import board
from digitalio import DigitalInOut, Direction, Pull
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control import ConsumerControl
# from adafruit_hid.consumer_control_code import ConsumerControlCode
import rotaryio

print("---Pico Magic Box Keyboard---")

"""
TIMER CLASS
"""


class cTimer:
    def __init__(self):
        self._start_time = None
        self._elapsed_time = 0.0

    def start(self):
        """Start a new timer"""
        if self._start_time is not None:
            # print(f"Timer is running. Use .stop() to stop it")
            return
        self._start_time = time.monotonic_ns()

    def getET(self):
        if self._start_time:
            self._elapsed_time = time.monotonic_ns() - self._start_time
        else:
            self._elapsed_time = 0
        return self._elapsed_time*1e-9  # in seconds

    def reset(self):
        self._start_time = time.monotonic_ns()
        self._elapsed_time = 0.0

    def stop(self):
        """Stop the timer, and report the elapsed time"""
        if self._start_time is None:
            # print(f"Timer is not running. Use .start() to start it")
            return
        self._start_time = None
        self._elapsed_time = 0.0
        print(f"Elapsed time: {self._elapsed_time:0.4f} seconds")


"""
END TIMER CLASS
"""

def int_to_list_bit_msb_lsb(val : int) -> list:
    # 0=MSB 3=LSB
    return [int(x) for x in '{0:04b}'.format(val)]


kbd = Keyboard(usb_hid.devices)
cc = ConsumerControl(usb_hid.devices)
MEDIA = 1
KEY = 2

""" WHEEL ENCODER JOG """
encoder = rotaryio.IncrementalEncoder(board.GP27, board.GP28)
time.sleep(0.1)
enc_last_position = encoder.position
enc_current_position = enc_last_position

print("---Configure PIN IO---")
""" DIRECT PINS """
pins = (
    board.GP0,  # indietro veloce (ad ogni pressione x2 x4 x8 x16 x32 x64)(shift+j)
    board.GP1,  # avanti veloce (ad ogni pressione x2 x4 x8 x16 x32 x64)(shift+l)
    board.GP2,  # stop (k)
    board.GP3,  # play/pause (ad ogni pressione play o pausa)(backspace)
    board.GP4,  # elezione timeline o mediapool (ad ogni pressione o l'uno o l'altro)(q)
    board.GP5,  # traccia video su (ctrl+shift+freccia su)
    board.GP6,  # traccia video giu (ctrl+shift+freccia giu)
    board.GP7,  # inserisci clip (append) (shift+f12)
    board.GP8,  # inserisci clip sopra (place on top) (f12)
)
NUM_OF_DIRECT_PINS = len(pins)
print(f"---N. of Direct Pins: {NUM_OF_DIRECT_PINS}---")
# GUI is also known as the Windows key, Command (Mac), or Meta
keymap = {
    (0): (KEY, (Keycode.SHIFT, Keycode.J)),
    (1): (KEY, (Keycode.SHIFT, Keycode.L)),
    (2): (KEY, [Keycode.K]),
    (3): (KEY, [Keycode.SPACE]),
    (4): (KEY, [Keycode.Q]),
    (5): (KEY, (Keycode.CONTROL, Keycode.SHIFT, Keycode.UP_ARROW)),
    (6): (KEY, (Keycode.CONTROL, Keycode.SHIFT, Keycode.DOWN_ARROW)),
    (7): (KEY, (Keycode.SHIFT, Keycode.F12)),
    (8): (KEY, [Keycode.F12]),
}
switches = []
for i in range(NUM_OF_DIRECT_PINS):
    switch = DigitalInOut(pins[i])
    switch.direction = Direction.INPUT
    switch.pull = Pull.UP
    switches.append(switch)
switch_state = NUM_OF_DIRECT_PINS * [0]
print(f"---switch_state: {switch_state}---")

""" MUX PINS """
# OUTPUT MUX SELECTORS # MSB - LSB
pins_mux_selector = (board.GP19, board.GP18, board.GP17, board.GP16)
mux_sel = []  # MSB= id.0 - LSB= id.3
for i in range(len(pins_mux_selector)):
    mux_s = DigitalInOut(pins_mux_selector[i])
    mux_s.direction = Direction.OUTPUT
    mux_s.value = False
    mux_sel.append(mux_s)
# MUX INPUT PIN
mux_in = DigitalInOut(board.GP20)
mux_in.direction = Direction.INPUT
mux_in.pull = Pull.UP
mux_switch_state = 16 * [0]
mux_keymap = {
    (0): (KEY, (Keycode.CONTROL, Keycode.Z)),  # annulla (ctrl+z)
    (1): (
        KEY,
        (Keycode.CONTROL, Keycode.SHIFT, Keycode.Z),
    ),  # Ripristina (ctrl+shift+z)
    (2): (KEY, [Keycode.SEMICOLON]),  # muovi clip indietro (;)
    (3): (KEY, [Keycode.PERIOD]),  # muovi clip avanti (.)
    (4): (KEY, (Keycode.ALT, Keycode.UP_ARROW)),  # muovi clip su (alt+freccia su)
    (5): (KEY, (Keycode.ALT, Keycode.DOWN_ARROW)),  # muovi clip giu(alt+freccia giu)
    (6): (
        KEY,
        (Keycode.CONTROL, Keycode.UP_ARROW),
    ),  # muovi selezione su (ctrl+ freccia su)
    (7): (
        KEY,
        (Keycode.CONTROL, Keycode.DOWN_ARROW),
    ),  # muovi selezione giu (ctrl+ freccia giu)
    (8): (
        KEY,
        (Keycode.CONTROL, Keycode.LEFT_ARROW),
    ),  # muovi selezione sinistra (ctrl+ freccia sx)
    (9): (
        KEY,
        (Keycode.CONTROL, Keycode.RIGHT_ARROW),
    ),  # muovi selezione destra (ctrl+ freccia dx)
    (10): (KEY, (Keycode.SHIFT, Keycode.V)),  # selezione clip (shift+v)
    (11): (KEY, (Keycode.ALT, Keycode.A)),  # Cancella clip  (alt+a)
    (12): (
        KEY,
        [Keycode.DELETE],
    ),  # cancella clip e elimina spazio (ripple delete)(canc)
    (13): (
        KEY,
        (Keycode.SHIFT, Keycode.Y),
    ),  # cancella clip prima del cursore (shift+y)
    (14): (KEY, (Keycode.SHIFT, Keycode.U)),  # cancella clip dopo il cursore (shift+u)
    (15): (KEY, (Keycode.CONTROL, Keycode.BACKSLASH)),  # taglia (ctrl+\)
}

loop_timer = cTimer()
loop_timer.start()
LOOP_KEYS_TIME = 0.02  # IN SEC

loop_jog = cTimer()
loop_jog.start()
LOOP_JOG_TIME = 0.02  # IN SEC
# EACH "SENSITIVITY" IMPULSES MOVE BY 1
# => e.g.: EACH 6 JOG STEPS EXECUTE 1 PRESS OF THE ARROW
SENSITIVITY = 1
print("---Run---")
while True:
    # loop every 0.05s = 50ms
    if loop_timer.getET() > LOOP_KEYS_TIME:
        loop_timer.reset()
        # DIRECT PINS
        for button in range(NUM_OF_DIRECT_PINS):
            if switch_state[button] == 0:
                if not switches[button].value:
                    try:
                        if keymap[button][0] == KEY:
                            kbd.press(*keymap[button][1])
                            print("---Direct Pressed---")
                        else:
                            cc.send(keymap[button][1])
                    except ValueError as ex:  # deals w six key limit
                        print(f"[ERR]: {ex}")
                    switch_state[button] = 1
            if switch_state[button] == 1:
                if switches[button].value:
                    try:
                        if keymap[button][0] == KEY:
                            kbd.release(*keymap[button][1])
                            print("---Direct Released---")
                    except ValueError as ex:
                        print(f"[ERR]: {ex}")
                    switch_state[button] = 0

        # MUX PINS
        for i in range(16):
            mux_cmd = int_to_list_bit_msb_lsb(val=i)
            # set the mux selectors
            for s in range(4):
                mux_sel[s].value = bool(mux_cmd[s])  # 0=MSB 3=LSB
            if mux_switch_state[i] == 0:
                # read the input
                if not mux_in.value:
                    try:
                        if mux_keymap[i][0] == KEY:
                            kbd.press(*mux_keymap[i][1])
                            print("---Mux Pressed---")
                        else:
                            cc.send(mux_keymap[i][1])
                    except ValueError as ex:  # deals w six key limit
                        print(f"[ERR]: {ex}")
                    mux_switch_state[i] = 1
            if mux_switch_state[i] == 1:
                if mux_in.value:
                    try:
                        if mux_keymap[i][0] == KEY:
                            kbd.release(*mux_keymap[i][1])
                            print("---Mux Released---")
                    except ValueError as ex:
                        print(f"[ERR]: {ex}")
                    mux_switch_state[i] = 0

    if loop_jog.getET() >= LOOP_JOG_TIME:
        loop_jog.reset()
        enc_current_position = encoder.position
        enc_position_change = int(enc_current_position - enc_last_position)
        if enc_position_change >= SENSITIVITY:
            kbd.send(Keycode.RIGHT_ARROW)  # send=press+release all
            enc_last_position = enc_current_position
            print(f"enc pos changed: {enc_position_change}")
        elif enc_position_change <= -SENSITIVITY:
            kbd.send(Keycode.LEFT_ARROW)  # send=press+release all
            enc_last_position = enc_current_position
            print(f"enc pos changed: {enc_position_change}")
        '''
        if enc_position_change > 0:
            for _ in range(enc_position_change):
                # cc.send(ConsumerControlCode.VOLUME_INCREMENT)
                kbd.send(Keycode.RIGHT_ARROW)
            print(f"enc pos changed: {enc_position_change}")
        elif enc_position_change < 0:
            for _ in range(-enc_position_change):
                # cc.send(ConsumerControlCode.VOLUME_DECREMENT)
                kbd.send(Keycode.LEFT_ARROW)
            print(f"enc pos changed: {enc_position_change}")
        enc_last_position = enc_current_position
        '''


