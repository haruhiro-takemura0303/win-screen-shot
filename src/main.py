import pyautogui
from PIL import ImageGrab, Image
import win32clipboard
from pynput import mouse
import io
import sys
import os
import json

# 実行時に引数を受け取る 
args = sys.argv[1:]

left_up_x = 100
left_up_y = 100 
right_down_x = 100
right_down_y = 100

class Param:
    def __init__(self):
        self.state = 0
        self.left_up_x = 0
        self.left_up_y = 0
        self.right_down_x = 0
        self.right_down_y = 0

def on_click(x, y, button, pressed):
    global state
    if pressed:
        if Param.state == 1:
            Param.left_up_x, Param.left_up_y = pyautogui.position()
            print("> Click Right Douwn")
            Param.state = 2
        elif Param.state == 2:
            Param.right_down_x, Param.right_down_y  = pyautogui.position()
            Param.state = 0
            print("Finish Setting")
            print("Left UP    : {0}, {1}".format(Param.left_up_x, Param.left_up_y))
            print("Right Down : {0}, {1}".format(Param.right_down_x, Param.right_down_y))
            ## Write Param
            # Read
            with open(r'.\src\position.json', 'r') as f:
                dict_json = json.load(f)
                dict_json['LeftUp']['x']    = Param.left_up_x
                dict_json['LeftUp']['y']    = Param.left_up_y
                dict_json['RightDown']['x'] = Param.right_down_x
                dict_json['RightDown']['y'] = Param.right_down_y
            # Write
            with open(r'.\src\position.json', 'r') as f:
                f = open(r'.\src\position.json', 'w')
                json.dump(dict_json,f ,indent=4)

            return False

def set_position():
    print("#-----Set Param-----------")
    print("> Click Left Up")
    Param.state = 1
    with mouse.Listener( on_click=on_click) as listener:
        listener.join()

def InitParam():
    with open(r'.\src\position.json', 'r') as f:
        dict_json = json.load(f)
        Param.left_up_x = dict_json['LeftUp']['x']
        Param.left_up_y = dict_json['LeftUp']['y']
        Param.right_down_x = dict_json['RightDown']['x']
        Param.right_down_y = dict_json['RightDown']['y']
        
def copy_to_clipboard():
    # Open Img
    original_image = Image.open('tmp.png')
    # Conv Bit Stream
    output = io.BytesIO()
    original_image.convert('RGB').save(output, 'BMP')
    data = output.getvalue()[14:]
    output.close()
    # Copy ClipBoard
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
    win32clipboard.CloseClipboard()
    # clear temp
    #os.remove("tmp.png")

def main():
    if "set" in args:
        set_position()
    else:
        # take screenshot
        InitParam()
        im = pyautogui.screenshot("tmp.png", region=(int(Param.left_up_x), 
                                                     int(Param.left_up_y), 
                                                     int(Param.right_down_x - Param.left_up_x), 
                                                     int(Param.right_down_y - Param.left_up_y)))
        copy_to_clipboard()
        os.remove("tmp.png")

if __name__ == "__main__":
    main()
