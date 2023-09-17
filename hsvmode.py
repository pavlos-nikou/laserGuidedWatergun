import cv2
import numpy as np
import time as t
import tkinter as tk
from tkinter import ttk
import sys
# import serial
import requests




def motor_down():
    #ser.write(b'd')  # 2-4-8 low 7high
    return


def motor_up():
    #for i in range(15):
        #ser.write(b'u')  # 2-4-7 low 8high
    return


def motor_left():
    #for i in range(15):
        #ser.write(b'l')
    return


def motor_right():
    #for i in range(15):
        #ser.write(b'r')  # 2-7-8 low 4high
    return


def motor_downright():
    #for i in range(15):
        #ser.write(b'q')  # 2-8 low  4-7 high
    return


def motor_downleft():
    #for i in range(15):
        #ser.write(b'g')  # 4-8 low 2-7 high
    return


def motor_upright():
    #for i in range(15):
        #ser.write(b'e')  # 2-7 low 4-8 high
    return


def motor_upleft():
    #for i in range(15):
        #ser.write(b't')  # 4-7 low 2-8 high
    return


def motor_stop():
    #for i in range(10):
        #ser.write(b's')  # 2-4-7-8 low
    return


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

def nothing(x):
    pass

def filter(frame):
    lh = cv2.getTrackbarPos("l-h", "trackbars")
    ls = cv2.getTrackbarPos("l-s", "trackbars")
    lv = cv2.getTrackbarPos("l-v", "trackbars")
    mh = cv2.getTrackbarPos("m-h", "trackbars")
    ms = cv2.getTrackbarPos("m-s", "trackbars")
    mv = cv2.getTrackbarPos("m-v", "trackbars")

    min = np.array([lh, ls, lv])
    max = np.array([mh, ms, mv])
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv,min,max)
    cv2.imshow("hsv",hsv)
    cv2.imshow("mask",mask)
    cv2.imshow("frame",frame)

def error_window(error):
    errorwin = tk.Tk()
    errorwin.title("error")
    errorwin.geometry("300x100+700+500")
    errormes = tk.Label(errorwin, text=error, font=("Courier", 15))
    errormes.place(height=100, width=250, x=30, y=0)
    return
def initiate():
    c = str(ac.get())
    c = int(c)
    cap = cv2.VideoCapture(url)
    # try:
    #     img_resp = requests.get(url)
    #     img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
    #     frame = cv2.imdecode(img_arr, -1)
    # except:
    #     error = "No Video Input"
    #     error_window(error)
    #     return
    cv2.namedWindow("trackbars")
    cv2.createTrackbar("l-h", "trackbars", 0, 179, nothing)
    cv2.createTrackbar("l-s", "trackbars", 0, 255, nothing)
    cv2.createTrackbar("l-v", "trackbars", 0, 255, nothing)
    cv2.createTrackbar("m-h", "trackbars", 179, 179, nothing)
    cv2.createTrackbar("m-s", "trackbars", 255, 255, nothing)
    cv2.createTrackbar("m-v", "trackbars", 255, 255, nothing)

    # targer = list(str(res.get()).split("x"))
    # targer[1] = int(int(targer[1]) / 2) + shifty
    # targer[0] = int(int(targer[0]) / 2) + shiftx
    ret, frame = cap.read()
    x = int(len(frame[0]) / 2)
    y = int(len(frame) / 2)
    print("x=", x, "y=", y)
    while True:
        targer = [y, x]  # if tracker stops you go in the middle
        # img_resp = requests.get(url)
        ret, frame = cap.read()
        lh = cv2.getTrackbarPos("l-h", "trackbars")
        ls = cv2.getTrackbarPos("l-s", "trackbars")
        lv = cv2.getTrackbarPos("l-v", "trackbars")
        mh = cv2.getTrackbarPos("m-h", "trackbars")
        ms = cv2.getTrackbarPos("m-s", "trackbars")
        mv = cv2.getTrackbarPos("m-v", "trackbars")
        min = np.array([lh, ls, lv])
        max = np.array([mh, ms, mv])
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, min, max)
        target = np.argwhere(mask == 255)

        if len(target) == 0:
            f1 = ((abs(targer[0] - y)) / y)
            f1c = color(f1)
            f2 = ((abs(targer[1] - x)) / x)
            f2c = color(f2)
            cv2.circle(frame, (targer[1], targer[0]), 10, (255, 1, 1), 1)
        else:
            center = int(int(len(target))/2)
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
                        (0, 255, 0), 1)
            cv2.putText(frame, str(240 - targer[0] + shifty), (targer[1], targer[0] - 15), cv2.FONT_ITALIC, 0.5,
                        (0, 255, 0), 1)
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
                    motor_downright()
                elif targer[0] < y - c:
                    cv2.putText(frame, "motorY U", (30, 50), cv2.FONT_ITALIC, 0.5, (0, 255, 0), 1)
                    motor_upright()
                else:
                    cv2.putText(frame, "motorY S", (30, 50), cv2.FONT_ITALIC, 0.5, (0, 255, 0), 1)
                    motor_right()

            elif targer[1] < x - c:
                cv2.putText(frame, "motorX L", (30, 30), cv2.FONT_ITALIC, 0.5, (0, 255, 0), 1)
                if targer[0] > y + c:
                    cv2.putText(frame, "motorY D", (30, 50), cv2.FONT_ITALIC, 0.5, (0, 255, 0), 1)
                    motor_downleft()
                elif targer[0] < y - c:
                    cv2.putText(frame, "motorY U", (30, 50), cv2.FONT_ITALIC, 0.5, (0, 255, 0), 1)
                    motor_upleft()
                else:
                    cv2.putText(frame, "motorY S", (30, 50), cv2.FONT_ITALIC, 0.5, (0, 255, 0), 1)
                    motor_left()
            else:
                cv2.putText(frame, "motorX S", (30, 30), cv2.FONT_ITALIC, 0.5, (0, 255, 0), 1)
                if targer[0] > y + c:
                    cv2.putText(frame, "motorY D", (30, 50), cv2.FONT_ITALIC, 0.5, (0, 255, 0), 1)
                    motor_down()
                elif targer[0] < y - c:
                    cv2.putText(frame, "motorY U", (30, 50), cv2.FONT_ITALIC, 0.5, (0, 255, 0), 1)
                    motor_up()
                else:
                    cv2.putText(frame, "motorY S", (30, 50), cv2.FONT_ITALIC, 0.5, (0, 255, 0), 1)
                    motor_stop()

            # for y

        cv2.imshow("frame", frame)
        cv2.imshow("threshold",mask)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break


def calibrate():
    global shifty, shiftx
    shifty = int(caliby_E.get())
    shiftx = int(calibx_E.get())
    return


if __name__ == "__main__":
    url = "http://192.168.178.32:4747/video"
    #ser = serial.Serial("com5", 9600)
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