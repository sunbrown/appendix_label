from myui import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtGui import QPainter, QPixmap, QPen, QPolygon, QPainterPath, QPolygonF, QWheelEvent
from PyQt5.QtCore import Qt, QPoint
import os
import shutil
import sys
import pandas as pd
import csv

class mywindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.setupUi(self)
        self.label = Winform(self.widget)
        self.gridLayout_3.addWidget(self.label)
        self.directory = []  # 文件根目录
        self.file_list = []  # 存储所有文件的文件名
        self.img_path = ''  # 当前文件路径
        self.im_idx = 0  # 文件序号
        self.file_num = 0  # 文件总数
        self.flag4 = []
        self.info_1 = ''
        self.info_2 = ''

        self.done = 0
        self.split_path = []
        self.img_name = ''
        self.ck_id = int
        self.root = ''
        self.dir = ''
        self.history = int
        self.history_path = './history.txt'
        self.save_root = 'D:/result'
        self.save_dir = ''
        self.csv_out_path = './label_result.csv'
        self.count = 0
        self.all_count = 0
        self.create_csv()
        self.create_history()
        self.csv_in = [0, 6, '双层', '液体', '有', '无', '无', '无', '无', '有', 1, 'H']

        self.start.clicked.connect(self.open_all)  # 打开图像文件路径
        self.pushButton_2.clicked.connect(self.btn2)
        self.pushButton_3.clicked.connect(self.btn3)
        self.pushButton_4.clicked.connect(self.btn4)
        self.pushButton_5.clicked.connect(self.btn5)
        self.pushButton_6.clicked.connect(self.btn6)
        self.pushButton_7.clicked.connect(self.btn7)
        self.pushButton_8.clicked.connect(self.btn8)
        self.pushButton_9.clicked.connect(self.btn9)
        self.pushButton_10.clicked.connect(self.btn10)

    def create_csv(self):
        if not os.path.exists(self.csv_out_path):
            df2 = pd.DataFrame(columns=['Check_ID', '直径', '管壁层次', '阑尾腔内', '周围系膜肿胀', '周围肿胀形式', '回盲部肠管肿胀',\
                                        '腹腔游离积液', '淋巴结胀大', '肠管扩张', '阑尾炎类别', '成像角度'])
            df2.to_csv(self.csv_out_path, index=False, encoding='gbk')

    # 读取进度文件（history.txt）
    def create_history(self):
        if os.path.exists(self.history_path):
            ff = open(self.history_path, 'r+')
            ff.seek(0)
            history = ff.read()
            if history:
                self.im_idx = int(history)
            else:
                self.im_idx = 0
            ff.close()
        else:  # 进度文件不存在创建一个
            ff = open(self.history_path, 'w+')
            ff.close()



    # 保存进度（把self.im_dex保存在history.txt中）
    def save_history(self):
        with open(self.history_path, 'w+') as ff:
            ff.seek(0)
            ff.truncate()
            ff.write(str(self.im_idx))

    # 主函数（处理文件self.img_path）
    def main_process(self):
        try:
            self.img_path = self.file_list[self.im_idx]
            self.label.pix = QPixmap(self.img_path)
            self.label.msk = QPixmap(self.img_path)
            self.label.msk.fill(Qt.black)

            self.split_path = self.img_path.split('\\')
            self.img_name = self.split_path[-1]
            self.ck_id = self.split_path[-2]
            # self.root = '\\'.join(self.split_path[0:-1])
            self.root = self.split_path[0]
            self.dir = '\\'.join(self.split_path[1:-1])
            self.save_dir = os.path.join(self.save_root, self.dir)
            (self.count, self.all_count, self.flag4) = self.where_now()
            self.info_1 = '总数:{3},当前总进度:{4}\n检查号:{0},病人进度:{1}/{2}'.\
                format(self.ck_id, self.count, self.all_count, self.file_num, self.im_idx+1)
            self.info_2 = '按R重画，按空格下一张或者跳过，按Q上一张(需要重新运行程序)，按ESC退出'
            self.textBrowser_1.setText(self.info_1)
            df = pd.read_csv('appendix2008-2018.csv', encoding='gbk')
            a1 = df.DN[df.ID == str(self.ck_id)]
            a2 = df.RS[df.ID == str(self.ck_id)]
            a3 = df.DES[df.ID == str(self.ck_id)]
            self.textBrowser_3.clear()
            for i1 in a1:
                try:
                    self.textBrowser_3.append(i1)
                except TypeError:
                    pass
            for i2 in a2:
                try:
                    self.textBrowser_3.append(i2)
                except TypeError:
                    pass
            for i3 in a3:
                try:
                    self.textBrowser_3.append(i3)
                except TypeError:
                    pass
            self.change_color()

        except IndexError:
            self.msg1()

    def change_color(self):
        if self.flag4[0]:
            self.label0.setStyleSheet("background-color: rgb(255, 255, 255);")
        else:
            self.label0.setStyleSheet("background-color: rgb(255, 97, 0);")
        if self.flag4[1]:
            self.label1.setStyleSheet("background-color: rgb(255, 255, 255);")
        else:
            self.label1.setStyleSheet("background-color: rgb(255, 97, 0);")
        if self.flag4[2]:
            self.label2.setStyleSheet("background-color: rgb(255, 255, 255);")
        else:
            self.label2.setStyleSheet("background-color: rgb(255, 97, 0);")
        if self.flag4[3]:
            self.label3.setStyleSheet("background-color: rgb(255, 255, 255);")
        else:
            self.label3.setStyleSheet("background-color: rgb(255, 97, 0);")

    def refresh(self):
        self.main_process()
        self.label.points_list = []
        # self.label.msk.fill(Qt.black)
        self.label.update()
        self.label.msk_flag = False
        self.save_history()
        self.csv_in[0] = self.ck_id
        self.csv_in[1] = self.spinBox.text()
        self.csv_in[11] = self.label.mouse_flag

    def save_csv(self):
        # with open(self.csv_out_path) as ff2:
        df1 = pd.read_csv(self.csv_out_path, encoding='gbk')
        # insertRow = pd.DataFrame(self.csv_in)
        # a = df1.loc[df1.Check_ID == str(self.ck_id)]
        idx = df1[df1.Check_ID == str(self.ck_id)].index
        if len(idx) == 0:
            df1.loc[len(df1)] = self.csv_in
        else:
            df1.loc[idx] = self.csv_in
        df1.to_csv(self.csv_out_path, index=False, encoding='gbk')

    def update_info2(self):
        info = '提示：鼠标左、右键分别勾画横、纵断灰阶图，按S键保存，滚轮切换图片（不保存）。键盘A、D键分别保存横断、纵断彩色原图图片'


    def where_now(self):
        name_list = []
        for root1, dirs1, files1 in os.walk(os.path.join(self.root, self.dir)):
            for file1 in files1:
                if os.path.splitext(file1)[1] == ".jpg":
                    name_list.append(file1)
        a = name_list.index(self.img_name) + 1
        b = len(name_list)

        for root2, dirs2, files2 in os.walk(self.save_dir):
            for file2 in files2:
                name_list.append(file2)
        flag = [0, 0, 0, 0]
        flag[0] = 'H.png' in name_list
        flag[1] = 'V.png' in name_list
        flag[2] = 'C_H.jpg' in name_list
        flag[3] = 'C_V.jpg' in name_list
        return a, b, flag

    def open_all(self):
        directory = QFileDialog.getExistingDirectory(self, "选择文件夹", "/")
        if directory == '':
            pass
        else:
            self.directory = directory
            self.file_list = self.listing_img(self.directory)  # 存储所有文件的文件名
            self.file_num = len(self.file_list)
            self.main_process()

    def msg1(self):
        info = "点“Yes”清除历史进度重新勾画！\n点击“Open”选择文件夹继续勾画！"
        reply = QMessageBox().information(self, "温馨提示^_^", info, QMessageBox.Yes | QMessageBox.Open | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.im_idx = 0
            self.main_process()
        elif reply == QMessageBox.Open:
            self.open_all()
        else:
            pass

    def btn2(self):
        # self.pushButton_2.setStyleSheet("background-color: rgb(255, 255, 255);")
        dic2 = {'双层': '紊乱', '紊乱': '正常', '正常': '双层'}
        self.label_2.setText(dic2.get(self.label_2.text()))
        self.csv_in[2] = self.label_2.text()

    def btn3(self):
        # self.pushButton_3.setStyleSheet("background-color: rgb(255, 255, 255);")
        dic3 = {'液体': '气体', '气体': '粪石', '粪石': '液体'}
        self.label_3.setText(dic3.get(self.label_3.text()))
        self.csv_in[3] = self.label_3.text()

    def btn4(self):
        # self.pushButton_4.setStyleSheet("background-color: rgb(255, 255, 255);")
        dic4 = {'有': '无', '无': '有'}
        self.label_4.setText(dic4.get(self.label_4.text()))
        self.csv_in[4] = self.label_4.text()

    def btn5(self):
        # self.pushButton_5.setStyleSheet("background-color: rgb(255, 255, 255);")
        dic5 = {'有': '无', '无': '有'}
        self.label_5.setText(dic5.get(self.label_5.text()))
        self.csv_in[5] = self.label_5.text()

    def btn6(self):
        # self.pushButton_6.setStyleSheet("background-color: rgb(255, 255, 255);")
        dic6 = {'有': '无', '无': '有'}
        self.label_6.setText(dic6.get(self.label_6.text()))
        self.csv_in[6] = self.label_6.text()

    def btn7(self):
        # self.pushButton_7.setStyleSheet("background-color: rgb(255, 255, 255);")
        dic7 = {'有': '无', '无': '有'}
        self.label_7.setText(dic7.get(self.label_7.text()))
        self.csv_in[7] = self.label_7.text()

    def btn8(self):
        # self.pushButton_8.setStyleSheet("background-color: rgb(255, 255, 255);")
        dic8 = {'有': '无', '无': '有'}
        self.label_8.setText(dic8.get(self.label_8.text()))
        self.csv_in[8] = self.label_8.text()

    def btn9(self):
        # self.pushButton_9.setStyleSheet("background-color: rgb(255, 255, 255);")
        dic9 = {'有': '无', '无': '有'}
        self.label_9.setText(dic9.get(self.label_9.text()))
        self.csv_in[9] = self.label_9.text()

    def btn10(self):
        # self.pushButton_10.setStyleSheet("background-color: rgb(255, 255, 255);")
        dic10 = {'1': '2', '2': '3', '3': '4', '4': '5', '5': '1'}
        dic11 = {'1': '单纯性阑尾炎', '2': '化脓性阑尾炎', '3': '化脓性伴灶性坏疽', '4': '坏疽性阑尾炎', '5': '阑尾脓肿'}
        self.label_10.setText(dic10.get(self.label_10.text()))
        self.label_11.setText(dic11.get(self.label_10.text()))
        self.csv_in[10] = self.label_10.text()

    def wheelEvent(self, event):
        # a = event.angleDelta()
        num = int(event.angleDelta().y()/120)
        for i in range(abs(num)):
            if num > 0:
                try:
                    self.im_idx -= 1
                    if self.im_idx < 0:
                        self.im_idx = 0
                    self.refresh()
                except IndexError:
                    pass
            else:
                try:
                    self.im_idx += 1
                    if self.im_idx > self.file_num - 1:
                        self.im_idx = self.file_num - 1
                    self.refresh()
                except IndexError:
                    pass

    def down_folder(self):
        try:
            self.im_idx += (self.all_count - self.count + 1)
            if self.im_idx > self.file_num - 1:
                self.im_idx = self.file_num - 1
            self.refresh()
        except IndexError:
            pass

    def up_folder(self):
        try:
            self.im_idx -= (self.count + 1)
            if self.im_idx < 0:
                self.im_idx = 0
            self.refresh()
        except IndexError:
            pass

    # 键盘事件
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.save_history()
            self.close()
        if event.key() == Qt.Key_Q:  # A键上一张
            try:
                self.im_idx -= 1
                if self.im_idx < 0:
                    self.im_idx = 0
                self.refresh()
            except IndexError:
                pass
        if event.key() == Qt.Key_E:  # D键下一张
            try:
                self.im_idx += 1
                if self.im_idx > self.file_num - 1:
                    self.im_idx = self.file_num - 1
                self.refresh()
            except IndexError:
                pass
        if event.key() == Qt.Key_R:  #
            self.up_folder()
        if event.key() == Qt.Key_F:  #
            self.down_folder()
        if event.key() == Qt.Key_W:  # W键删除mask
            try:
                self.refresh()
            except FileNotFoundError or IndexError:
                pass
        if event.key() == Qt.Key_S:  # S键保存mask、下一张
            try:
                if not os.path.exists(self.save_dir):
                    os.makedirs(self.save_dir)
                self.label.msk.save(self.save_dir + '\\' + self.label.mouse_flag + '.png')
                self.im_idx += 1
                if self.im_idx > self.file_num - 1:
                    self.im_idx = self.file_num - 1
                self.refresh()
                self.save_csv()
            except FileNotFoundError or IndexError:
                pass
        if event.key() == Qt.Key_A:  # Q键保存彩色图C_H.jpg
            try:
                if not os.path.exists(self.save_dir):
                    os.makedirs(self.save_dir)
                dist = self.save_dir + '\\' + 'C_H.jpg'
                shutil.copyfile(self.img_path, dist)
                self.im_idx += 1
                if self.im_idx > self.file_num - 1:
                    self.im_idx = self.file_num - 1
                self.refresh()
            except IOError:
                pass
        if event.key() == Qt.Key_D:  # Q键保存彩色图C_H.jpg
            try:
                if not os.path.exists(self.save_dir):
                    os.makedirs(self.save_dir)
                dist = self.save_dir + '\\' + 'C_V.jpg'
                shutil.copyfile(self.img_path, dist)
                self.im_idx += 1
                if self.im_idx > self.file_num - 1:
                    self.im_idx = self.file_num - 1
                self.refresh()
            except IOError:
                pass

    # 列出所有jpg文件
    def listing_img(self, in_path):
        name_list = []
        for root1, dirs1, files1 in os.walk(in_path):
            for file1 in files1:
                if os.path.splitext(file1)[1] == ".jpg":
                    path1 = os.path.join(root1, file1)
                    name_list.append(path1)
        return name_list


class Winform(QWidget):
    def __init__(self, parent=None):
        super(Winform, self).__init__(parent)
        # self.initUi()
        self.pix = QPixmap()  # 实例化一个 QPixmap 对象
        self.Point_1 = QPoint()  # 起始点
        self.Point_2 = QPoint()  # 终点
        self.pen1 = QPen()  # 定义笔格式对象
        self.pen2 = QPen()
        self.pen1.setWidth(2)  # 设置笔的宽度
        self.pen2.setWidth(2)  # 设置笔的宽度
        self.pen1.setColor(Qt.red)
        self.pen2.setColor(Qt.blue)
        self.points_list = []
        self.points_list1 = []
        self.mouse_flag = 'H'
        self.msk_flag = True
        self.msk = QPixmap(1024, 768)
        self.msk.fill(Qt.black)
        self.polygon = QPolygon()
        self.path = QPainterPath()

    # 绘图函数
    def paintEvent(self, event):
        painter0 = QPainter(self)
        painter1 = QPainter(self.pix)
        painter2 = QPainter(self.msk)

        if self.mouse_flag == 'H':
            painter1.setPen(self.pen1)
        else:
            painter1.setPen(self.pen2)

        for iii in range(len(self.points_list) - 1):
            painter1.drawLine(self.points_list[iii], self.points_list[iii + 1])
        painter0.drawPixmap(0, 0, self.pix)  # 在画布上画出

        if self.msk_flag:
            for iii in range(len(self.points_list) - 1):
                self.polygon.append(self.points_list[iii])
            self.path.addPolygon(QPolygonF(self.polygon))
            painter2.setBrush(Qt.white)
            painter2.fillPath(self.path, Qt.white)
            self.points_list = []
            self.polygon = QPolygon()
            self.path = QPainterPath()

    # 鼠标按压事件
    def mousePressEvent(self, event):
        # 鼠标左右键按下
        if event.button() == Qt.LeftButton:
            self.mouse_flag = 'H'
            self.msk_flag = False
            self.points_list.append(event.pos())
        if event.button() == Qt.RightButton:
            self.mouse_flag = 'V'
            self.msk_flag = False
            self.points_list.append(event.pos())

    # 鼠标移动事件
    def mouseMoveEvent(self, event):
        # 鼠标左键按下的同时移动鼠标
        if event.buttons() and (Qt.LeftButton or Qt.RightButton):
            self.points_list.append(event.pos())
            self.msk_flag = False
            self.update()

    # 鼠标释放事件
    def mouseReleaseEvent(self, event):
        # 鼠标左键释放
        if event.button() == Qt.LeftButton or Qt.RightButton:
            self.points_list.append(self.points_list[0])
            self.msk_flag = True
            self.update()


if __name__ == "__main__":
    save_root = r'D:\\result'
    app = QApplication(sys.argv)
    window = mywindow()
    window.show()
    sys.exit(app.exec_())
