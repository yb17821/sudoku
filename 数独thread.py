import copy
import queue
import pyautogui
import readpage
import threading
import time


# def duqu(hlx, path):  # 从文本文档读取内容
#     lbs = []
#     lbc = []
#     with open(path) as f:
#         for row in range(hlx):
#             for col in range(hlx):
#                 num = f.read(1)
#                 if num != "0":
#                     lbs.append(num)
#                 else:
#                     lbs.append("123456789")  # 必须这样,否则变量会有问题
#             f.read(1)
#             lbc.append(lbs)
#             lbs = []
#     print("读取成功")
#     return lbc


def xieru(list):
    pyautogui.click()
    for row in range(9):
        for col in range(9):
            pyautogui.press(list[row][col])
            pyautogui.press("tab")


def shoujidanxiang(list):  # 收集单独数字
    danxiang = {}
    for row in range(9):
        for col in range(9):
            if len(list[row][col]) == 1:
                danxiang[str(row) + str(col)] = list[row][col]
    return danxiang


def shoujijihe(list):  # 收集行，列，块的元素集合
    dich = {}
    dicl = {}
    dicq = {}
    for num in range(9):
        dich[num] = ""
        dicl[num] = ""
        dicq[num] = ""
    lt = copy.deepcopy(list)
    for row in range(9):
        for col in range(9):
            dicq[row // 3 * 3 + col // 3] += lt[row][col]
            dich[row] += lt[row][col]
            dicl[col] += lt[row][col]
    return dich, dicl, dicq


def jiance(list):  # 检测是否出现重复值
    lt = copy.deepcopy(list)
    dich, dicl, dicq = shoujijihe(lt)
    for row in range(9):
        for col in range(9):
            if len(lt[row][col]) == 1:
                if dich[row].count(lt[row][col]) > 1:
                    # print(row,"行错了，错误值为",lt[row][col])
                    return False
                if dicl[col].count(lt[row][col]) > 1:
                    # print(col, "列错了，错误值为",lt[row][col])
                    return False
                if dicq[row // 3 * 3 + col // 3].count(lt[row][col]) > 1:
                    # print(row // 3 + col // 3 * 3, "号块错了，错误值为",lt[row][col])
                    return False
            elif len(lt[row][col]) == 0:
                # print( "{0}行{1}列有空白元素".format(row,col))
                return False
    return True


def dayi(list):  # 打印
    lt = []
    for i in list:
        for j in i:
            lt.append(j.ljust(4, " "))
        lt.append("\n")
    print("".join(lt))


def op(list):
    danxiang = shoujidanxiang(list)
    lt = copy.deepcopy(list)
    for row in range(9):
        for col in range(9):
            if len(lt[row][col]) > 1:
                for kcol in range(9):  # 清除同列
                    dx = danxiang.get(str(row) + str(kcol))
                    try:
                        lt[row][col] = lt[row][col].replace(dx, "")
                    except:
                        pass
                for krow in range(9):  # 清除同行
                    dx = danxiang.get(str(krow) + str(col))
                    try:
                        lt[row][col] = lt[row][col].replace(dx, "")
                    except:
                        pass
                if row in [0, 1, 2]:  # 清除同一区块
                    kuairow = [0, 1, 2]
                elif row in [3, 4, 5]:
                    kuairow = [3, 4, 5]
                else:
                    kuairow = [6, 7, 8]
                if col in [0, 1, 2]:
                    kuaicol = [0, 1, 2]
                elif col in [3, 4, 5]:
                    kuaicol = [3, 4, 5]
                else:
                    kuaicol = [6, 7, 8]
                for krow in kuairow:
                    for kcol in kuaicol:
                        if krow != row and kcol != col:
                            dx = danxiang.get(str(krow) + str(kcol))
                            try:
                                lt[row][col] = lt[row][col].replace(dx, "")
                            except:
                                pass
    dich, dicl, dicq = shoujijihe(lt)  # 取唯一值操作
    for row in range(9):
        for col in range(9):
            if len(lt[row][col]) > 1:
                for s in lt[row][col]:
                    if dich[row].count(s) == 1:
                        lt[row][col] = s
                        break
                    if dicl[col].count(s) == 1:
                        lt[row][col] = s
                        break
                    if dicq[row // 3 * 3 + col // 3].count(s) == 1:
                        lt[row][col] = s
                        break
    length1 = len(shoujidanxiang(list))
    length2 = len(shoujidanxiang(lt))
    if length2 != length1:
        # op(lt)
        return op(lt)
    else:
        # q.put(lt)
        return lt


def main(list):
    global tim
    # op(list)
    # ltt = q.get()
    ltt = op(list)
    # print("-----------------------操作完毕，等待检测--------------------------------")
    # dayi(ltt)
    if jiance(ltt):
        length1 = len(shoujidanxiang(ltt))
        if length1 != 81:
            for row in range(9):
                for col in range(9):
                    if len(ltt[row][col]) > 1:
                        string = copy.copy(ltt[row][col])
                        for num in string:
                            ltt[row][col] = num
                            print(threading.current_thread().name, "号线程尝试，共", tim, "次")
                            tim += 1
                            # print("----------------------未出错，进行尝试--------------------------------")
                            # dayi(ltt)
                            if daan.empty():
                                main(ltt)
                            else:
                                # print(threading.current_thread().name,"答案出来了，线程结束")
                                exit()  # 用来结束线程
        elif daan.empty():
            daan.put(ltt)
            if threading.current_thread().name == "1":
                ltt2 = ltt
            elif threading.current_thread().name == "2":
                ltt2 = turn(ltt, 3)
            elif threading.current_thread().name == "3":
                ltt2 = turn(ltt, 2)
            else:
                ltt2 = turn(ltt, 1)

            print(threading.current_thread().name, "号线程得到----------------------- 答案--------------------------------")
            dayi(ltt2)
            xieru(ltt2)  # 写到网页上
            # pyautogui.click((404, 915))
            exit()
    else:
        # print("---------------------检测出错--------------------------------")
        return


def turn(lt, t):
    lt2 = []
    if t == 0:
        return lt
    for col in range(9):
        lt1 = []
        for row in range(8, -1, -1):
            lt1.append(lt[row][col])
        lt2.append(lt1)
    return turn(lt2, t - 1)


if __name__ == "__main__":
    print('5秒后开始')
    time.sleep(5)
    path = r"C:\Users\Administrator\Desktop\1.txt"
    daan = queue.Queue(maxsize=1)
    tim = 1

    # 自动循环做题
    # pos = pyautogui.position()
    # while True:
    #     while True:
    #         if pyautogui.pixelMatchesColor(588,549,(255, 255, 255)):
    #             break
    #         time.sleep(0.2)
    #     ltstart1 = readpage.du(path)
    #     ltstart2 = turn(ltstart1, 1)
    #     ltstart3 = turn(ltstart1, 2)
    #     ltstart4 = turn(ltstart1, 3)
    #     args = [ltstart1,ltstart2,ltstart3,ltstart4]
    #     for i in range(len(args)):
    #         one = threading.Thread(target=main,name = str(i+1),args=(args[i],))
    #         one.start()
    #     while True:
    #         if pyautogui.pixelMatchesColor(588,549,(173, 173, 173)):
    #             pyautogui.press("enter")
    #             break
    #         time.sleep(0.2)
    #     daan.get()
    #     pyautogui.moveTo(pos)
    #     exit()

    # 单线程
    # one = threading.Thread(target=main,args=(ltstart1,))
    # one.start()
    # pyautogui.pixelMatchesColor(588,549,(173, 173, 173))

    # 多线程
    ltstart1 = readpage.du(path)
    ltstart2 = turn(ltstart1, 1)
    ltstart3 = turn(ltstart1, 2)
    ltstart4 = turn(ltstart1, 3)
    args = [ltstart1, ltstart2, ltstart3, ltstart4]
    for i in range(len(args)):
        one = threading.Thread(target=main, name=str(i + 1), args=(args[i],))
        one.start()
