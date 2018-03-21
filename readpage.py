import win32clipboard as w
import win32con
import pyautogui
import re
def getCopyText():
    w.OpenClipboard()
    copy_text = w.GetClipboardData(win32con.CF_TEXT)
    w.CloseClipboard()
    return copy_text.decode('GB2312')

def du(path):
    pos = pyautogui.position()
    pyautogui.click((pos[0] - 100, pos[1]))
    pyautogui.dragRel(550, 400)
    pyautogui.hotkey("ctrl", "c")
    lt = getCopyText()
    lt = re.compile("\n").split(lt)
    lt[-2] = "\r"
    lt = iter(lt[13:-1])
    rowlt = []
    collt = []
    while True:
        try:
            line = next(lt)
            if line[0].isdecimal():
                collt.append(line[0])
                next(lt)
            else:
                collt.append("123456789")
            if len(collt) == 9:
                rowlt.append(collt)
                collt = []
        except:
            break
    #将处理的内容写入txt文件，非必要步骤
    # with open(path,"w") as f:
    #     for row in range(9):
    #         for col in range(9):
    #             if rowlt[row][col].isdecimal():
    #                 f.write(rowlt[row][col])
    #             else:
    #                 f.write("0")
    #         f.write("\n")
    pyautogui.click(pos)
    return rowlt

if __name__ == "__main__":
    path= r"C:\Users\Administrator\Desktop\1.txt"
    du(path)











