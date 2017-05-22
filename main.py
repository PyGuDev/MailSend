# -*- coding: utf-8 -*-
from tkinter import *
from tkinter.filedialog import *
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
import smtplib
import mimetypes


class Main_UI:
    # главный графический интерфейс
    def __init__(self, _mainroot):
        self.is_active = False
        self.varSt = IntVar()
        self.varLog = IntVar()
        self.varSt.set(0)
        self.varLog.set(0)
        self.EmailToUser = ""
        # главное окно
        self.mainRoot = _mainroot
        self.mainRoot.maxsize(width=640, height=420)
        self.mainRoot.minsize(width=640, height=420)
        self.mainRoot.geometry("640x420")
        self.mainRoot.title("Mail send")
        self.frameMain = Frame(self.mainRoot, width=640, height=420, bg="#00C0FF")
        self.frameMain.pack()
        # текст названия
        self.lableTitleMain = Label(self.frameMain, text="Mail dispatch", bg="#00C0FF", fg="white", font=((), 30))
        self.lableTitleMain.place(x=222.5, y=10)
        # виджет ввода текста
        self.text = Text(self.frameMain, width=70, height=10, bg="white", fg="black", wrap=WORD)
        self.text.place(x=70, y=100)
        # кнопки
        self.butSend = Button(self.frameMain, bg="black", text="Отправить")
        self.butSend.place(x=242, y=320)
        self.butClear = Button(self.frameMain, text="Очистить")
        self.butClear.place(x=340, y=320)
        self.butToUser = Button(self.frameMain, text="Кому")
        self.butToUser.place(x=179, y=320)
        self.butExit = Button(self.frameMain, text="Выход")
        self.butExit.place(x=430, y=320)
        self.butAttach = Button(self.frameMain, text="Прикрепить")
        self.butAttach.place(x=70, y=270)
        # события кнопок
        self.butToUser.bind("<Button-1>", self.toUserUi)
        self.butClear.bind("<Button-1>", self.clear_text)
        self.butSend.bind("<Button-1>", self.sendText)
        self.butExit.bind("<Button-1>", self.quit_mainUi)
        self.butAttach.bind("<Button-1>", self.click_butAttach)
        # окно входа
        self.login_ui()

    # окно email получателя письма
    def toUserUi(self, event):
        self.userRoot = Toplevel(self.mainRoot)
        self.userRoot.title("To user")
        self.lableEmailToUser = Label(self.userRoot, text="Email")
        self.lableEmailToUser.grid(row=0, column=0)
        self.entryEmailToUser = Entry(self.userRoot, width=40)
        self.entryEmailToUser.grid(row=0, column=1)
        self.lableUserNameToUser = Label(self.userRoot, text="Name")
        self.lableUserNameToUser.grid(row=1, column=0)
        self.entryUserNameToUser = Entry(self.userRoot, width=40)
        self.entryUserNameToUser.grid(row=1, column=1)
        self.check = Checkbutton(self.userRoot, text="Стандартный набор", variable=self.varSt)
        self.check.grid(row=2, column=0)
        self.butQuit = Button(self.userRoot, text="Ok")
        self.butQuit.grid(row=3, column=0)
        self.butQuit.bind("<Button-1>", self.quit_toUserUi)

    # окно авторизации
    def login_ui(self):
        self.root = Toplevel(self.mainRoot)
        self.root.title("Mail send")
        self.root.minsize(width=400, height=320)
        self.root.maxsize(width=400, height=320)
        self.lableTitle = Label(self.root, text="Mail dispatch", width=20, font=((), 20), bg="black", fg="white")
        self.lableLogin = Label(self.root, text="Email", fg="black")
        self.entryLogin = Entry(self.root, width=20)
        self.lablePass = Label(self.root, text="Password", fg="black")
        self.entryPass = Entry(self.root, width=20, show='*')
        self.butLogin = Button(self.root, text="Вход")
        self.lableResul = Label(self.root, text="Ожидание")
        self.checkLogin = Checkbutton(self.root, text="Запомнить", variable=self.varLog)

        self.lableTitle.place(x=65, y=10)
        self.lableLogin.place(x=10 + 50, y=50 + 40)
        self.entryLogin.place(x=80 + 50, y=50 + 40)
        self.lablePass.place(x=10 + 50, y=90 + 40)
        self.entryPass.place(x=80 + 50, y=90 + 40)
        self.butLogin.place(x=130 + 10, y=120 + 40)
        self.lableResul.place(x=175, y=190)
        self.checkLogin.place(x=220, y=165)
        try:
            self.fR = open("key.txt", 'r')
        except FileNotFoundError:
            self.fR = open("key.txt", 'w+')
        else:
            if self.fR != '':
                try:
                    user, pas, checkValue = self.fR.read().split(" ")
                except ValueError:
                    self.fR.close()
                else:
                    self.varLog.set(int(checkValue))
                    if self.varLog.get() == 1:
                        self.entryLogin.configure(cursor="xterm")
                        self.entryPass.configure(cursor="xterm")
                        self.entryLogin.insert(0, user)
                        self.entryPass.insert(0, pas)
                    self.fR.close()
            else:
                self.fR.close()
        self.butLogin.bind("<Button-1>", self.click_Login)


    # функция подключени и авторизации с сервером
    def login(self, _user, _pas):
        self.server = smtplib.SMTP("smtp.gmail.com", 587)  # подключение к серверу
        self.server.ehlo()
        self.server.starttls()
        self.username = _user  # Имя пользователя
        self.password = _pas  # Пароль
        self.message =MIMEMultipart()
        # проверка на ошибки
        try:
            self.server.login(self.username, self.password)  # авторизация с сервером
        except smtplib.SMTPAuthenticationError:
            return False
        else:
            self.serverWorking = True  # авторизован
            return True

    def click_Login(self, event):
        # проверка заполнены ли поля login
        if self.varLog.get() == 0:
            if self.entryLogin.get() == "":
                self.lableResul["text"] = "Введите login!"
                self.lableResul["fg"] = "red"
            elif self.searchRusSym(self.entryLogin.get()) != 0:
                self.lableResul["text"] = "Введите коректный login!"
                self.lableResul["fg"] = "red"
            else:
                # взятие логина из поля
                self.user = self.entryLogin.get()
                self.lableResul["text"] = "Ожидание"
                self.lableResul["fg"] = "black"
            # проверка заполнены ли поля pass
            if self.entryPass.get() == "":
                self.lableResul["text"] = "Введите password!"
                self.lableResul["fg"] = "red"

            elif self.searchRusSym(self.entryPass.get()) != 0:
                self.lableResul["text"] = "Введите коректный password!"
                self.lableResul["fg"] = "red"
            else:
                # взятие пароля из поля
                self.pas = self.entryPass.get()
                self.lableResul["text"] = "Ожидание"
                self.lableResul["fg"] = "black"
                # проверка входа
                if not self.login(self.user, self.pas):
                    self.lableResul["text"] = "Ошибка"
                    self.lableResul["fg"] = "red"
                else:
                    self.lableResul["text"] = "Вошли"
                    self.lableResul["fg"] = "green"
                    self.quit_ui()
                    # вошел ли ты
                    self.is_active = not self.is_active
        elif self.varLog.get() == 1:
            with open("key.txt", "r") as f:
                if f.read() != '' or f.read() == '':
                    if self.entryLogin.get() == "":
                        self.lableResul["text"] = "Введите login!"
                        self.lableResul["fg"] = "red"
                    elif self.searchRusSym(self.entryLogin.get()) != 0:
                        self.lableResul["text"] = "Введите коректный login!"
                        self.lableResul["fg"] = "red"
                    else:
                        # взятие логина из поля
                        self.user = self.entryLogin.get()
                        self.lableResul["text"] = "Ожидание"
                        self.lableResul["fg"] = "black"
                    # проверка заполнены ли поля pass
                    if self.entryPass.get() == "":
                        self.lableResul["text"] = "Введите password!"
                        self.lableResul["fg"] = "red"

                    elif self.searchRusSym(self.entryPass.get()) != 0:
                        self.lableResul["text"] = "Введите коректный password!"
                        self.lableResul["fg"] = "red"
                    else:
                        # взятие пароля из поля
                        self.pas = self.entryPass.get()
                        self.lableResul["text"] = "Ожидание"
                        self.lableResul["fg"] = "black"
                        # проверка входа
                        if not self.login(self.user, self.pas):
                            self.lableResul["text"] = "Ошибка"
                            self.lableResul["fg"] = "red"
                        else:
                            self.lableResul["text"] = "Вошли"
                            self.lableResul["fg"] = "green"
                            with open("key.txt", "w+") as fp:
                                fp.write(self.user + " " + self.pas + " " + str(self.varLog.get()))
                                self.quit_ui()
                                # вошел ли ты
                                self.is_active = not self.is_active
                                # закрытие окна авторизации

    # функция закрытия окна авторизации
    def quit_ui(self):
        self.root.destroy()

    # функция закрытия главного окна
    def quit_mainUi(self, event):
        if not self.is_active:
            self.mainRoot.quit()
        else:
            self.server.quit()
            self.mainRoot.quit()


    # функция закрытия окна toUser
    def quit_toUserUi(self, event):
        if self.varSt.get() == 0:
            self.EmailToUser = self.entryEmailToUser.get()
            self.UserName = self.entryUserNameToUser.get()
        elif self.varSt.get() == 1:
            self.EmailToUser = ["79279263082@yandex.ru","churkina.aniuta@yandex.ru", "vyugova13@gmail.com", "bikbulatova.milya@yandex.ru", "svetkinggg45@gmail.com", "gubaev1999@gmail.com"]
            self.UserName = self.entryUserNameToUser.get()
        self.userRoot.destroy()

    # функция очистки виджета text
    def clear_text(self, event):
        self.text.delete('1.0', END)

    # функция отправки письма
    def sendText(self, event):
        self.message["Subject"] = "Dispath"
        self.message["From"] = "Developer"
        self.message["To"] = "Test"
        self.text_msg = MIMEText(self.text.get('1.0', END), "text")
        self.message.attach(self.text_msg)
#        message = "\r\n".join([  # формируем сообщение Email с полями
#           "From: Developer",
#            "To: " + self.UserName,
#            "Subject: dispath",
#            "",
#            self.text.get('1.0', END),
#       ]).encode("utf-8")
        if type(self.EmailToUser) == type([]):
            for i in self.EmailToUser:
                self.server.sendmail(self.username, str(i), self.message.as_string())
        elif type(self.EmailToUser) == type(""):
            self.server.sendmail(self.username, self.EmailToUser, self.message.as_string())
        self.message = MIMEMultipart()

    def searchRusSym(self, str):
        count = 0
        for s in range(0, len(str)):
            if 1040 <= ord(str[s]) <= 1103:
                count += 1
        return count

    # открытие окна
    def open_dialog(self):
        op = askopenfilename()
        ctype, encoding = mimetypes.guess_type(op)
        self.maintype, self.subtype = ctype.split("/", 1)
        return op

    def click_butAttach(self, event):
        op = self.open_dialog()
        with open(op, 'rb') as file:
            if self.maintype == "text":
                self.attachment = MIMEText(file.read(), _subtype=self.subtype)
                file.close()
            elif self.maintype == "image":
                self.attachment = MIMEImage(file.read(), _subtype=self.subtype)
                file.close()
            elif self.maintype == "audio":
                self.attachment = MIMEAudio(file.read(), _subtype=self.subtype)
                file.close()
            self.attachment.add_header('Content-Disposition', 'attachment', filename=op)
            self.message.attach(self.attachment)
    def ld(self):
        if self.varLog.get() == 0:
            self.varLog.set(1)
        else:
            self.varLog.set(0)

# главная функция
def main():
    mainroot = Tk()
    Main_UI(mainroot)
    mainroot.mainloop()


if __name__ == "__main__":
    main()
