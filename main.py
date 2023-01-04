#导入模块
import tkinter
from tkinter import ttk         # 下拉选项框
from tkinter import messagebox
from tkinter import *
import threading
import datetime
from datetime import *
from time import sleep
import oppoint

class my_window(tkinter.Frame):
    # 调用时初始化
    def __init__(self):
        global win  # 全局变量
        # 创建主窗口
        win = tkinter.Tk()
        win.title("体育馆自动化预约工具")
        win.geometry("650x350+650+20")  # 长x宽+x*y
        win.resizable(0, 0)  # 窗口大小固定
        self.main_window()  #在窗口中创建元素的函数
        win.mainloop()

    # 创建token输入框
    def get_token(self):
        # 创建l1标签
        l1 = tkinter.Label(win, text='请输入token：', justify=tkinter.RIGHT, width=50)
        l1.place(x=20, y=40,  # 设置x，y坐标
                 width=100, height=30  # 设置长宽
                 )
        # 定义输入框
        global e1   #全局变量
        e1 = tkinter.Entry(win)
        e1.place(x=120, y=40, width=150, height=30) #place方法确定位置

    #创建选择时段的下拉选项框
    def get_time(self):
        # 创建lable2标签
        l2 = tkinter.Label(win, text='选择预约时段：', justify=tkinter.RIGHT, width=50)
        l2.place(x=20, y=100,  # 设置x，y坐标
                 width=100, height=30  # 设置长宽
                 )
        #创建下拉框
        value = tkinter.StringVar()
        values = ['18:30-19:30', "19:30-20:30", "20:30-21:30"]
        global combobox     # 全局变量
        combobox = ttk.Combobox(
            master=win,  # 父容器
            height=10,  # 高度,下拉显示的条目数量
            width=20,  # 宽度
            state='readonly',  # 设置状态 normal(可选可输入)、readonly(只可选)、 disabled
            cursor='arrow',  # 鼠标移动时样式 arrow, circle, cross, plus...
            font=('', 10),  # 字体
            textvariable=value,  # 通过StringVar设置可改变的值
            values=values,  # 设置下拉框的选项
        )
        combobox.place(x=120, y=100, width=150, height=30)  # place方法确定位置

    # 创建选择星期的复选框
    def get_week(self):
        # 创建lable3标签
        l3 = tkinter.Label(win, text='选择预约星期：', justify=tkinter.RIGHT, width=50)
        l3.place(x=20, y=160,  # 设置x，y坐标
                 width=100, height=30  # 设置长宽
                 )
        global checkVar1,checkVar2,checkVar3,checkVar4,checkVar5,checkVar6,checkVar7    #全局变量
        # 创建复选框组件
        # StringVar()是Tkinter下的对象，它支持将变量的值实时显示在屏幕上
        checkVar1 = StringVar(value="0")    # 默认复选框的值为“0”，显示出来即为不打√，如果为“1”，则默认打√
        checkbutton1 = tkinter.Checkbutton(win, text='星期一', variable=checkVar1)     # 创建复选框
        checkbutton1.place(x=120, y=160, width=60, height=30)   #place()方法定位
        checkVar2 = StringVar(value="0")
        checkbutton2 = tkinter.Checkbutton(win, text='星期二', variable=checkVar2)
        checkbutton2.place(x=200, y=160, width=60, height=30)
        checkVar3 = StringVar(value="0")
        checkbutton3 = tkinter.Checkbutton(win, text='星期三', variable=checkVar3)
        checkbutton3.place(x=120, y=190, width=60, height=30)
        checkVar4 = StringVar(value="0")
        checkbutton4 = tkinter.Checkbutton(win, text='星期四', variable=checkVar4)
        checkbutton4.place(x=200, y=190, width=60, height=30)
        checkVar5 = StringVar(value="0")
        checkbutton5 = tkinter.Checkbutton(win, text='星期五', variable=checkVar5)
        checkbutton5.place(x=120, y=220, width=60, height=30)
        checkVar6 = StringVar(value="0")
        checkbutton6 = tkinter.Checkbutton(win, text='星期六', variable=checkVar6)
        checkbutton6.place(x=200, y=220, width=60, height=30)
        checkVar7 = StringVar(value="0")
        checkbutton7 = tkinter.Checkbutton(win, text='星期天', variable=checkVar7)
        checkbutton7.place(x=120, y=250, width=60, height=30)

    # 创建日志文本框
    def creat_text(self):
        # 创建lable1标签
        l4 = tkinter.Label(win, text='日志：', justify=tkinter.RIGHT, width=50)
        l4.place(x=280, y=15,  # 设置x，y坐标
                 width=80, height=30  # 设置长宽
                 )
        # 创建文本框
        self.log = tkinter.Text(win)
        self.log.place(x=300, y=40, width=330, height=280)  # place()方法定位

    # get通过各组件得到的数据
    def get_val(self):
        messagebox.showinfo('', '提交成功')     # 弹框显示提交成功提示
        # 根据e1文本框输入获取token
        self.token = e1.get()
        # 根据时段下拉框的值确定将来请求时ptId的值，具体时段与ptId的对应关系，网站+F12，查看网页源代码可以看到
        if combobox.get() == '18:30-19:30':
            self.time = '18'
        elif combobox.get() == '19:30-20:30':
            self.time = '19'
        else:
            self.time = '20'
        # 根据复选框输入获取weekday
        self.week = [checkVar1.get(), checkVar2.get(), checkVar3.get(), checkVar4.get(), checkVar5.get(),
                     checkVar6.get(), checkVar7.get()]

    # 创建提交按钮
    def creat_btn(self):
        self.btn = Button(win, text='提交', command=self.start_thread)
        self.btn.place(x=230, y=300, width=50, height=20)  # 按钮布局

    # 整合一下，运行定义好的每个组件，这样的话在__init__中就只需要写main_window一个函数即可。
    def main_window(self):
        self.get_token()
        self.get_time()
        self.get_week()
        self.creat_text()
        self.creat_btn()

    # 运行keep_token方法，并在日志文本框中插入keep_token的运行结果
    # 抛弃之前用的schedule直接定时，转而用sleep定时
    def do_keep_token(self,token):
        while True: # 死循环，让程序一直运行
            self.log.insert(1.0,oppoint.keep_token(token))
            self.log.insert(1.0,'\n')
            sleep(60*10-10)

    # 运行oppoint方法，并在日志文本框中插入
    # 抛弃之前用的schedule定时，转而用sleep+判断定时
    # 虽然schedule很方便，但是对应在后面的包括定时任务以及非定时任务的多线程里就很难操作，无法适配需求。
    def do_oppoint(self,token,ptid,week,time):
        list = []
        # 获取week列表中的有效值，得到的list列表内容为用户需要预订的星期，格式为——例子：[2,3,5]，需要预订星期二、星期三和星期五。
        for i in range(len(week)):
            if week[i] == '1':
                list.append(i + 1)
        while True:     # 死循环让程序一直运行
            '''自己写的一个定时的小算法，主要利用获取当前时间与预订时间字符串比较来实现定时'''
            for i in range(len(list)):
                if list[i] == datetime.now().isoweekday():  # 判断当天星期是否在需要预约的星期列表中
                    # 获取当前日期时间
                    d = datetime.now()
                    # 类型转换成str，然后进行字符串分割、拼接的操作，得到当前时间“hour:minute”
                    s = str(d)
                    l1 = s.split(' ')
                    l2 = l1[1].split(':')
                    t = l2[0] + ':' + l2[1]
                    # 判断时间是否符合，执行目标函数
                    if t == time:
                        self.log.insert(1.0, oppoint.oppoint(token, ptid))
                        self.log.insert(1.0, '\n')
                        sleep(60 * 60 * 24 - 20)
                    else:
                        pass

    # 20220812230058046cs7o252qx5sbd9n
    # 实现多线程并行
    def start_thread(self):
        t = '06:51'     # 发送预约请求的时间
        self.get_val()       # 运行getVal()函数，获取用户在GUI上的输入
        # 定义两个线程，注意：args参数以元组存储，括号及后面的逗号不可省略，否则程序报错
        a1 = threading.Thread(target = self.do_keep_token,args = (self.token,))
        a2 = threading.Thread(target = self.do_oppoint, args = (self.token,self.time,self.week,t,))
        # 执行定义的线程
        a1.start()
        a2.start()

# 运行my_window()类
if __name__ == '__main__':
    my_window()