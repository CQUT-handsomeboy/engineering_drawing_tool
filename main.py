import cv2
import numpy as np
import tkinter as tk

from tkinter import simpledialog
from tkinter import messagebox


root = tk.Tk()
root.withdraw()

file_name = simpledialog.askstring(title="输入", prompt="文件名路径")

material = cv2.imread(file_name)

sh = int(simpledialog.askstring(title="输入", prompt="窗口高度设置"))

try:
    h, w = material.shape[:2]
except AttributeError:
    exit()

new_w = int(sh * (w / h))
new_h = sh

material = cv2.resize(material, (new_w, new_h))

set_positions = []
set_delta = None  # 实际像素点差值
set_value = None  # 图标注差值


def set_on_mouse(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:

        if len(set_positions) >= 2:
            set_positions.clear()

        set_positions.append((x, y))

        global set_delta
        if len(set_positions) == 2:
            delta_1 = abs((set_positions[0][0] - set_positions[1][0]))
            delta_2 = abs((set_positions[0][1] - set_positions[1][1]))

            if delta_1 > delta_2:
                set_delta = delta_1
            else:  # delta_2 > delta_1
                set_delta = delta_2

            messagebox.showinfo("提示", "设置成功!")

            cv2.setMouseCallback("main", normal_on_mouse)


normal_positions = []


def normal_on_mouse(event, x, y, flags, param):

    if event == cv2.EVENT_LBUTTONDOWN:

        if len(normal_positions) >= 2:
            normal_positions.clear()

        normal_positions.append((x, y))

        if len(normal_positions) == 2:

            delta_1 = abs((normal_positions[0][0] - normal_positions[1][0]))
            delta_2 = abs((normal_positions[0][1] - normal_positions[1][1]))

            if (set_delta is None) or (set_delta is None):
                return

            if delta_1 > delta_2:
                messagebox.showinfo(
                    "提示", f"测量值：{delta_1 / set_delta * set_value}"
                )
                print()
            else:  # delta_2 > delta_1
                messagebox.showinfo(
                    "提示", f"测量值：{delta_2 / set_delta * set_value}"
                )


cv2.namedWindow("main")
cv2.setMouseCallback("main", normal_on_mouse)

while 1:
    cv2.imshow("main", material)
    k = cv2.waitKey(100)
    if k == ord("s"):
        user_input = simpledialog.askstring(title="输入", prompt="输入设置的值")
        try:
            set_value = float(user_input)
        except ValueError:
            continue
        cv2.setMouseCallback("main", set_on_mouse)
    elif k == ord("q"):
        break

cv2.destroyAllWindows()
