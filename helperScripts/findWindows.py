import win32gui

def examine_window(hwnd, filtr=None):
    window_title = win32gui.GetWindowText(hwnd)
    window_class = win32gui.GetClassName(hwnd)

    if filtr is not None:
        if filtr in window_title:
            print(window_title.encode('ascii', 'ignore'), window_class.encode('ascii', 'ignore'), sep=" -- ")
    else:
        print(window_title.encode('ascii', 'ignore'), window_class.encode('ascii', 'ignore'), sep=" -- ")


print("To show all open programs")
print("press 1")
print("To filter, press 2")

choice = input("Input your answer: ")

if choice == "1":
    win32gui.EnumWindows(examine_window, None)
elif choice == "2":
    filtr = input("Type the text to filter for: ")
    win32gui.EnumWindows(examine_window, filtr)
