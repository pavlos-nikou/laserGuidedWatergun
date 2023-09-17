import cv2
import numpy as np
import time as t
import tkinter as tk
from tkinter import ttk
import serial
# import requests


def srdir(x, y):
    x = x + shiftx
    y = y + shifty
    print(x,y)
    data = str(x) + "," + str(y) + "\n"
    ser.write(data.encode())


def color(g):
    g = g * 100
    if g <= 33:
        g = (0, 255, 0)
    elif g <= 66:
        g = (0, 255, 255)
    else:
        g = (0, 0, 255)
    return g
    # cam dimentrions x0-640 y0-480


def error_window(error):
    errorwin = tk.Tk()
    errorwin.title("error")
    errorwin.geometry("300x100+700+500")
    errormes = tk.Label(errorwin, text=error, font=("Courier", 15))
    errormes.place(height=100, width=250, x=30, y=0)
    return


def initiate():
    # c = str(ac.get())
    c = int(5)
    cap = cv2.VideoCapture(url)
    # try:
    #     img_resp = requests.get(url)
    #     img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
    #     frame = cv2.imdecode(img_arr, -1)
    # except :
    #     error = "No Video Input"
    #     error_window(error)
    #     return

    ret, frame = cap.read()
    x = int(len(frame[0]) / 2) + shiftx
    y = int(len(frame) / 2) - shifty
    while True:
        tstart = t.time()
        targer = [y, x]  # if tracker stops you go in the middle
        # img_resp = requests.get(url)
        # img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
        # frame = cv2.imdecode(img_arr, -1)
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        retval, threshold = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY)
        target = np.argwhere(threshold == 255)

        if len(target) == 0:
            f1 = ((abs(targer[0] - y)) / y)
            f1c = color(f1)
            f2 = ((abs(targer[1] - x)) / x)
            f2c = color(f2)
            cv2.circle(frame, (targer[1], targer[0]), 10, (255, 1, 1), 1)
        else:
            targer = target[0]
            # print (targer)
            f1 = ((abs(y - targer[0])) / y)
            f1c = color(f1)
            f2 = ((abs(targer[1] - x)) / x)
            f2c = color(f2)
            cv2.circle(frame, (targer[1], targer[0]), 10, (255, 1, 1), 1)
            cv2.line(frame, (x, targer[0]), (targer[1], targer[0]), f2c, 1)
            cv2.line(frame, (targer[1], y), (targer[1], targer[0]), f1c, 1)
            cv2.putText(frame, str(targer[1] - 320 + shiftx), (targer[1] + 30, targer[0]), cv2.FONT_ITALIC, 0.5,
                        (255, 0, 0), 1)
            cv2.putText(frame, str(240 - targer[0] + shifty), (targer[1], targer[0] - 15), cv2.FONT_ITALIC, 0.5,
                        (255, 0, 0), 1)
        cv2.line(frame, (0, y), (4 * x, y), (0, 0, 0), 2)
        cv2.line(frame, (x, 0 - 320), (x, 4 * y), (0, 0, 0), 2)

        if switch.current() == 0:
            # for y
            persentf1 = str(int(f1 * 100)) + "%"
            cv2.putText(frame, persentf1, (110, 50), cv2.FONT_ITALIC, 0.5, f1c, 1)
            # for x
            persentf2 = str(int(f2 * 100)) + "%"
            cv2.putText(frame, persentf2, (110, 30), cv2.FONT_ITALIC, 0.5, f2c, 1)

            # for X
            if targer[1] > x + c:
                cv2.putText(frame, "motorX R", (30, 30), cv2.FONT_ITALIC, 0.5, (0, 255, 0), 1)
                if targer[0] > y + c:
                    cv2.putText(frame, "motorY D", (30, 50), cv2.FONT_ITALIC, 0.5, (0, 255, 0), 1)
                elif targer[0] < y - c:
                    cv2.putText(frame, "motorY U", (30, 50), cv2.FONT_ITALIC, 0.5, (0, 255, 0), 1)
                else:
                    cv2.putText(frame, "motorY S", (30, 50), cv2.FONT_ITALIC, 0.5, (0, 255, 0), 1)
            elif targer[1] < x - c:
                cv2.putText(frame, "motorX L", (30, 30), cv2.FONT_ITALIC, 0.5, (0, 255, 0), 1)
                if targer[0] > y + c:
                    cv2.putText(frame, "motorY D", (30, 50), cv2.FONT_ITALIC, 0.5, (0, 255, 0), 1)
                elif targer[0] < y - c:
                    cv2.putText(frame, "motorY U", (30, 50), cv2.FONT_ITALIC, 0.5, (0, 255, 0), 1)
                else:
                    cv2.putText(frame, "motorY S", (30, 50), cv2.FONT_ITALIC, 0.5, (0, 255, 0), 1)
            else:
                cv2.putText(frame, "motorX S", (30, 30), cv2.FONT_ITALIC, 0.5, (0, 255, 0), 1)
                if targer[0] > y + c:
                    cv2.putText(frame, "motorY D", (30, 50), cv2.FONT_ITALIC, 0.5, (0, 255, 0), 1)
                elif targer[0] < y - c:
                    cv2.putText(frame, "motorY U", (30, 50), cv2.FONT_ITALIC, 0.5, (0, 255, 0), 1)
                else:
                    cv2.putText(frame, "motorY S", (30, 50), cv2.FONT_ITALIC, 0.5, (0, 255, 0), 1)
            #srdir(targer[1], targer[0])
        frametime = t.time() - tstart
        fps = int(1 / frametime)
        cv2.putText(frame, str(fps), (2*x-30, 15), cv2.FONT_ITALIC, 0.5, (0, 255, 0), 1)
        cv2.imshow("frame", frame)
        # cv2.imshow("threshold",threshold)
        # cv2.imshow("gray",gray)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break


def calibrate():
    global shifty, shiftx
    shifty = int(caliby_E.get())
    shiftx = int(calibx_E.get())
    return


if __name__ == "__main__":
    url = "http://192.168.178.32:4747/video"
    #ser = serial.Serial("com4", 9600)
    shiftx = 0
    shifty = 0
    window = tk.Tk()
    window.title("LASER GUN")
    window.geometry("800x250+0+0")
    # buttons
    start_button = tk.Button(window, text="Start", command=initiate, font=("Courier", 15))
    start_button.place(height=40, width=100, x=150, y=35 + 80)

    calib_button = tk.Button(window, text="Calibrate", command=calibrate, font=("Courier", 15))
    calib_button.place(height=40, width=150, x=450, y=35 + 80)

    # labels
    accuracy = tk.Label(window, text="accuracy :", font=("Courier", 15))
    accuracy.place(height=50, width=145, x=10, y=25)

    caliby = tk.Label(window, text="pixel shift for y :", font=("Courier", 15))
    caliby.place(height=50, width=300, x=300, y=25)

    calibx = tk.Label(window, text="pixel shift for x :", font=("Courier", 15))
    calibx.place(height=50, width=300, x=300, y=60)

    motorctrl = tk.Label(window, text="Motors :", font=("Courier", 15))
    motorctrl.place(height=50, width=145, x=10, y=175)
    # entrys
    ac = tk.Entry(window)
    ac.place(height=25, width=100, x=150, y=40)

    caliby_E = tk.Entry(window)
    caliby_E.place(height=25, width=100, x=575, y=40)

    calibx_E = tk.Entry(window)
    calibx_E.place(height=25, width=100, x=575, y=73)

    # combobox
    switch = ttk.Combobox(window, values=["On", "Off"])
    switch.current(1)
    switch.place(height=25, width=100, x=150, y=187)

    window.mainloop()

    cv2.destroyAllWindows()
