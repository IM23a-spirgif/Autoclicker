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
    """Clears focus from entry when clicking anywhere else,
       except if clicking on an entry widget."""
    if event.widget not in (delay_entry, hotkey_entry):
        root.focus_set()


def open_config():
    """Opens the configuration menu by hiding the main frame and showing the config frame."""
    main_frame.pack_forget()
    config_frame.pack(fill=tk.BOTH, expand=True)


def close_config():
    """Closes the configuration menu, updates HOTKEY, and returns to the main UI."""
    global HOTKEY
    new_hotkey = hotkey_entry.get().strip()
    if new_hotkey:
        HOTKEY = KeyCode(char=new_hotkey[0])
        start_button.config(text=f"Start ({HOTKEY.char.upper()})")
        stop_button.config(text=f"Stop ({HOTKEY.char.upper()})")
        main_hotkey_label.config(text=f"Press '{HOTKEY.char}' to Start/Stop")
    config_frame.pack_forget()
    main_frame.pack(fill=tk.BOTH, expand=True)


root = tk.Tk()
root.title("Fretux' Autoclicker")
root.geometry("300x200")
root.eval('tk::PlaceWindow . center')
main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)
tk.Label(main_frame, text="Delay between clicks (seconds):").pack(pady=5)
delay_entry = tk.Entry(main_frame)
delay_entry.pack(pady=5)
delay_entry.insert(0, "0.5")
main_hotkey_label = tk.Label(main_frame, text=f"Press '{HOTKEY.char}' to Start/Stop")
main_hotkey_label.pack(pady=5)
button_frame = tk.Frame(main_frame)
button_frame.pack(pady=10)
start_button = tk.Button(button_frame, text=f"Start ({HOTKEY.char.upper()})", command=toggle_clicking, width=15)
stop_button = tk.Button(button_frame, text=f"Stop ({HOTKEY.char.upper()})", command=toggle_clicking, width=15)
start_button.pack(side=tk.LEFT, padx=5)
stop_button.pack(side=tk.LEFT, padx=5)
config_button = tk.Button(main_frame, text="Configure", command=open_config)
config_button.pack(pady=5)
config_frame = tk.Frame(root)
tk.Label(config_frame, text="Configure HOTKEY").pack(pady=10)
hotkey_entry = tk.Entry(config_frame)
hotkey_entry.pack(pady=5)
hotkey_entry.insert(0, HOTKEY.char)
back_button = tk.Button(config_frame, text="Back", command=close_config)
back_button.pack(pady=10)
root.bind("<Button-1>", clear_focus)
listener = Listener(on_press=on_key_press)
listener.start()
stop_button["state"] = DISABLED
root.mainloop()
