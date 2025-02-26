import tkinter as tk
from tkinter import DISABLED, NORMAL
from pynput.mouse import Controller, Button
from pynput.keyboard import Listener, KeyCode
import threading
import time

mouse = Controller()
clicking = False
HOTKEY = KeyCode(char='-')


def click_loop(delay):
    """Continuously clicks while clicking is True."""
    global clicking
    while clicking:
        mouse.click(Button.left, 1)
        time.sleep(delay)


def toggle_clicking():
    """Toggles the clicking state."""
    global clicking
    clicking = not clicking
    if clicking:
        try:
            delay = float(delay_entry.get())
        except ValueError:
            delay = 0.5
        thread = threading.Thread(target=click_loop, args=(delay,))
        thread.daemon = True
        thread.start()
    start_button.focus_set()
    root.focus_set()
    switch()


def switch():
    if clicking:
        start_button["state"] = DISABLED
        stop_button["state"] = NORMAL
    else:
        start_button["state"] = NORMAL
        stop_button["state"] = DISABLED


def on_key_press(key):
    """Handles keypress events to toggle clicking."""
    if key == HOTKEY:
        toggle_clicking()


def clear_focus(event):
    """Clears focus from entry when clicking anywhere else."""
    if event.widget != delay_entry:
        root.focus_set()


# GUI Setup
root = tk.Tk()
root.title("Fretux' Autoclicker")
root.geometry("300x150")
root.eval('tk::PlaceWindow . center')
config_button = tk.Button(root, text="Configure")
tk.Label(root, text="Delay between clicks (seconds):").pack()
delay_entry = tk.Entry(root)
delay_entry.pack()
delay_entry.insert(0, "0.5")
tk.Label(root, text=f"Press '{HOTKEY.char}' to Start/Stop").pack()
button_frame = tk.Frame(root)
button_frame.pack(pady=10)
start_button = tk.Button(button_frame, text=f"Start ({HOTKEY.char.upper()})", command=toggle_clicking, width=15)
stop_button = tk.Button(button_frame, text=f"Stop ({HOTKEY.char.upper()})", command=toggle_clicking, width=15)
start_button.pack(side=tk.LEFT, padx=5)
stop_button.pack(side=tk.LEFT, padx=5)
config_button.pack(side=tk.TOP, padx=5)
root.bind("<Button-1>", clear_focus)
listener = Listener(on_press=on_key_press)
listener.start()
stop_button["state"] = DISABLED
root.mainloop()
