#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import cg_algorithms as alg
from typing import Optional
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    qApp,
    QGraphicsScene,
    QGraphicsView,
    QGraphicsItem,
    QListWidget,
    QHBoxLayout,
    QWidget,
    QStyleOptionGraphicsItem)
from PyQt5.Qt import QColorDialog
from PyQt5.QtGui import QPainter, QMouseEvent, QColor, QPalette
from PyQt5.QtCore import QRectF

import math


class MyCanvas(QGraphicsView):
    """
    画布窗体类，继承自QGraphicsView，采用QGraphicsView、QGraphicsScene、QGraphicsItem的绘图框架
    """
    def __init__(self, *args):
        super().__init__(*args)
        self.main_window = None
        self.list_widget = None
        self.item_dict = {}
        self.selected_id = ''

        self.status = ''
        self.temp_algorithm = ''
        self.temp_id = ''
        self.temp_item = None
        self.temp_index = 1
        self.color = None
        self.temp_coordination = []
        self.operation = ''
        self.origan_p_list = []

    def showItemSelected(self):
        x0, y0 = self.temp_coordination[0]
        x1, y1 = self.temp_coordination[1]
        if (x0 > x1):
            x0, x1 = x1, x0
        if (y0 > y1):
            y0, y1 = y1, y0
        s = abs(x0 - x1) * abs(y0 - y1)
        maxSum = 0
        maxItem = -1
        for index in self.item_dict.keys():
            tempSum = 0
            item = self.item_dict[index]
            a0, b0 = item.p_list[0]
            a1, b1 = item.p_list[1]
            for xx, yy in item.p_list:
                a0 = min(a0, xx)
                a1 = max(a1, xx)
                b0 = min(b0, xx)
                b1 = max(b1, xx)
            if a0 == a1:
                a1 = a1 + 1
            if b0 == b1:
                b1 = b1 + 1
            s1 = abs(a0 - a1) * abs(b0 - b1)
            l0 = x1 - x0 + a1 - a0 - max(x0, x1, a0, a1) + min(x0, x1, a0, a1)
            if (l0 < 0):
                l0 = 0
            l1 = y1 - y0 + b1 - b0 - max(y0, y1, b0, b1) + min(y0, y1, b0, b1)
            if (l1 < 0):
                l1 = 0
            s2 = l1 * l0
            if (s + s1 -s2 == 0):
                tempSum = 0
            else:
                tempSum = s2 * 1.0 / (s + s1 - s2)
            print('index:{}  tempSum:{}'.format(index, tempSum))
            if (tempSum > maxSum):
                maxSum = tempSum
                maxItem = index
        #print(maxSum)
        if (maxItem == -1):
            maxItem = self.selected_id
        if (maxItem != ''):
            self.clear_selection()
            self.selection_changed(maxItem)

    def start_draw_line(self, algorithm, item_id, color):
        self.status = 'line'
        self.temp_algorithm = algorithm
        self.temp_id = item_id
        self.color = color

    def start_draw_polygon(self, algorithm, item_id, color):
        self.status = 'polygon'
        self.temp_algorithm = algorithm
        self.temp_id = item_id
        self.color = color

    def start_draw_ellipse(self, item_id, color):
        self.status = 'ellipse'
        self.temp_algorithm = ''
        self.temp_id = item_id
        self.color = color

    def start_draw_curve(self, algorithm, item_id, color):
        self.status = 'curve'
        self.temp_algorithm = algorithm
        self.temp_id = item_id
        self.color = color

    def start_select_item(self):
        self.status = 'select'
        self.temp_algorithm = ''

    def start_translate_item(self):
        self.status = 'translate'
        self.temp_algorithm = ''

    def start_rotate_item(self):
        self.status = 'rotate'
        self.temp_algorithm = ''

    def start_scale_item(self):
        self.status = 'scale'
        self.temp_algorithm = ''

    def start_clip_item(self, algorithm):
        if self.selected_id not in self.item_dict.keys():
            self.status = ''
            return
        item = self.item_dict[self.selected_id]
        if (item.item_type == 'line'):
            print('it is a line')
            self.status = 'clip'
            self.temp_algorithm = algorithm
        else:
            self.status = ''

    def finish_draw(self):
        self.temp_id = self.main_window.get_id()

    def calculate_degree(self, x0, y0, x1, y1):
        l0 = math.sqrt(x0 * x0 + y0 * y0)
        l1 = math.sqrt(x1 * x1 + y1 * y1)
        if (l0 == 0 or l1 == 0):
            return 0
        cosa = (x0 * x1 + y0 * y1) * 1.0 / l0 / l1
        if (cosa >= 1):
            return 0
        r = math.acos(cosa)
        if (x0 * y1 - x1 * y0 == 0):
            x0 = x0 + 1
        if (x0 * y1 - x1 * y0 < 0):
            r = 2 * math.pi - r
        return int(r * 180 / math.pi)

    def calculate_times(self, x0, y0, x1, y1):
        l0 = math.sqrt(x0 * x0 + y0 * y0)
        l1 = math.sqrt(x1 * x1 + y1 * y1)
        #print(l1 / l0)
        if l0 == 0:
            l0 = 1
        return l1 / l0

    def clear_selection(self):
        if self.selected_id != '':
            self.item_dict[self.selected_id].selected = False
            self.selected_id = ''

    def clear_canvas(self):
        self.list_widget.clear()
        self.item_dict = {}
        self.selected_id = ''

        self.status = ''
        self.temp_algorithm = ''
        self.temp_id = ''
        self.temp_item = None
        self.temp_index = 1
        self.color = None
        self.temp_coordination = []
        self.operation = ''
        self.origan_p_list = []

    def selection_changed(self, selected):
        if selected not in self.item_dict.keys():
            return
        self.main_window.statusBar().showMessage('图元选择： %s' % selected)
        if self.selected_id != '':
            self.item_dict[self.selected_id].selected = False
            self.item_dict[self.selected_id].update()
        self.selected_id = selected
        self.item_dict[selected].selected = True
        self.item_dict[selected].update()
        #self.status = ''
        self.updateScene([self.sceneRect()])

    def mousePressEvent(self, event: QMouseEvent) -> None:
        pos = self.mapToScene(event.localPos().toPoint())
        x = int(pos.x())
        y = int(pos.y())
        if self.status == 'line':
            self.temp_item = MyItem(self.temp_id, self.status, [[x, y], [x, y], self.color], self.temp_algorithm)
            self.scene().addItem(self.temp_item)
        elif self.status == 'polygon' or self.status == 'curve':
            if (event.button() == 1):
                if self.temp_index == 1:
                    self.temp_item = MyItem(self.temp_id, self.status, [[x, y], [x, y], self.color], self.temp_algorithm)
                    self.scene().addItem(self.temp_item)
                else:
                    self.temp_item.p_list[self.temp_index] = [x, y]
            elif (event.button() == 2):
                if self.temp_index <= 1:
                    pass
                else:
                    self.temp_item.p_list.pop()
                    if (len(self.temp_item.p_list) > 3 or self.status == 'polygon'):
                        self.item_dict[self.temp_id] = self.temp_item
                        #print('final')
                        #print(self.temp_item.p_list)
                        self.list_widget.addItem(self.temp_id)
                        self.finish_draw()
                self.temp_index = 0
        elif self.status == 'ellipse':
            self.temp_item = MyItem(self.temp_id, self.status, [[x, y], [x, y], self.color], self.temp_algorithm)
            self.scene().addItem(self.temp_item)
        elif self.status == 'select':
            self.temp_coordination = [[x, y], [x, y]]
        elif self.status == 'translate':
            self.temp_coordination = [[x, y], [x, y]]
        elif self.status == 'rotate':
            if self.temp_index == 1:
                self.temp_coordination = [[x, y], [x, y]]
                self.origan_p_list = self.item_dict[self.selected_id].p_list
            else:
                self.temp_coordination[self.temp_index] = [x,y]
        elif self.status == 'scale':
            if self.temp_index == 1:
                self.temp_coordination = [[x, y], [x, y]]
                self.origan_p_list = self.item_dict[self.selected_id].p_list
            else:
                self.temp_coordination[self.temp_index] = [x,y]
        elif self.status == 'clip':
            self.temp_coordination = [[x, y], [x, y]]

        self.updateScene([self.sceneRect()])
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        pos = self.mapToScene(event.localPos().toPoint())
        x = int(pos.x())
        y = int(pos.y())
        if self.status == 'line':
            self.temp_item.p_list[1] = [x, y]
        elif self.status == 'polygon' or self.status == 'curve':
            self.temp_item.p_list[self.temp_index] = [x, y]
        elif self.status == 'ellipse':
            self.temp_item.p_list[1] = [x, y]
        elif self.status == 'select':
            self.temp_coordination[1] = [x, y]
            self.showItemSelected()
        elif self.status == 'translate':
            x0, y0 = self.temp_coordination[0]
            self.item_dict[self.selected_id].p_list = \
                alg.translate(self.item_dict[self.selected_id].p_list,
                              x - x0, y - y0)
            self.temp_coordination[0] = [x, y]
        elif self.status == 'rotate':
            if (self.temp_index == 1):
                self.temp_coordination[1] = [x, y]
            else:
                xc, yc = self.temp_coordination[0]
                x0, y0 = self.temp_coordination[1]
                r = self.calculate_degree(x0 - xc, y0 - yc, x - xc, y - yc)
                self.item_dict[self.selected_id].p_list = \
                    alg.rotate(self.origan_p_list,
                               xc, yc, r)
        elif self.status == 'scale':
            if (self.temp_index == 1):
                self.temp_coordination[1] = [x, y]
            else:
                xc, yc = self.temp_coordination[0]
                x0, y0 = self.temp_coordination[1]
                s = self.calculate_times(x0 - xc, y0 - yc, x - xc, y - yc)
                self.item_dict[self.selected_id].p_list = \
                    alg.scale(self.origan_p_list,
                               xc, yc, s)
        elif self.status == 'clip':
            self.temp_coordination[1] = [x, y]

        self.updateScene([self.sceneRect()])
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if self.status == 'line':
            self.item_dict[self.temp_id] = self.temp_item
            self.list_widget.addItem(self.temp_id)
            self.finish_draw()
        elif self.status == 'polygon' or self.status == 'curve':
            if (self.temp_index != 0):
                pos = self.mapToScene(event.localPos().toPoint())
                x = int(pos.x())
                y = int(pos.y())
                self.temp_item.p_list.append([x, y])
                #print(self.temp_item.p_list)
            self.temp_index = self.temp_index + 1
        elif self.status == 'ellipse':
            self.item_dict[self.temp_id] = self.temp_item
            self.list_widget.addItem(self.temp_id)
            self.finish_draw()
        elif self.status == 'select':
            pass
        elif self.status == 'translate':
            pass
        elif self.status == 'rotate':
            pos = self.mapToScene(event.localPos().toPoint())
            x = int(pos.x())
            y = int(pos.y())
            if (self.temp_index == 1):
                self.temp_coordination.append([x, y])
                self.temp_index = 2
            else:
                xc, yc = self.temp_coordination[0]
                x0, y0 = self.temp_coordination[1]
                r = self.calculate_degree(x0 - xc, y0 - yc, x - xc, y - yc)
                self.item_dict[self.selected_id].p_list = \
                    alg.rotate(self.origan_p_list,
                               xc, yc, r)
                self.updateScene([self.sceneRect()])
                self.temp_index = 1
        elif self.status == 'scale':
            pos = self.mapToScene(event.localPos().toPoint())
            x = int(pos.x())
            y = int(pos.y())
            if (self.temp_index == 1):
                self.temp_coordination.append([x, y])
                self.temp_index = 2
            else:
                xc, yc = self.temp_coordination[0]
                x0, y0 = self.temp_coordination[1]
                s = self.calculate_times(x0 - xc, y0 - yc, x - xc, y - yc)
                self.item_dict[self.selected_id].p_list = \
                    alg.scale(self.origan_p_list,
                               xc, yc, s)
                self.updateScene([self.sceneRect()])
                self.temp_index = 1
        elif self.status == 'clip':
            x0, y0 = self.temp_coordination[0]
            x1, y1 = self.temp_coordination[1]
            temp_p_list = \
                alg.clip(self.item_dict[self.selected_id].p_list,
                         min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1),
                         self.temp_algorithm)
            if temp_p_list != None:
                self.item_dict[self.selected_id].p_list = temp_p_list
            else:
                selected = self.selected_id
                self.clear_selection()
                self.list_widget.clearSelection()
                self.scene().removeItem(self.item_dict[selected])
                for index in range(self.list_widget.count()):
                    item = self.list_widget.item(index)
                    #print('{} {}'.format(item.text(), index))
                    #print(item.text())
                    if item.text() == selected:
                        self.list_widget.takeItem(index)
                        del item
                        break
                '''
                for index in self.item_dict.keys():
                    print('add{}'.format(index))
                    self.scene().addItem(self.item_dict[index])
                '''
                self.status = ''


            self.updateScene([self.sceneRect()])
        super().mouseReleaseEvent(event)


class MyItem(QGraphicsItem):
    """
    自定义图元类，继承自QGraphicsItem
    """
    def __init__(self, item_id: str, item_type: str, p_list: list, algorithm: str = '', parent: QGraphicsItem = None):
        """
        :param item_id: 图元ID
        :param item_type: 图元类型，'line'、'polygon'、'ellipse'、'curve'等
        :param p_list: 图元参数
        :param algorithm: 绘制算法，'DDA'、'Bresenham'、'Bezier'、'B-spline'等
        :param parent:
        """
        super().__init__(parent)
        self.id = item_id           # 图元ID
        self.item_type = item_type  # 图元类型，'line'、'polygon'、'ellipse'、'curve'等
        self.color = p_list.pop()

        self.p_list = p_list      # 图元参数
        self.algorithm = algorithm  # 绘制算法，'DDA'、'Bresenham'、'Bezier'、'B-spline'等
        self.selected = False


    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: Optional[QWidget] = ...) -> None:
        if self.item_type == 'line':
            item_pixels = alg.draw_line(self.p_list, self.algorithm)
            for p in item_pixels:
                painter.setPen(self.color)
                painter.drawPoint(*p)
            if self.selected:
                painter.setPen(QColor(255, 0, 0))
                painter.drawRect(self.boundingRect())
        elif self.item_type == 'polygon':
            item_pixels = alg.draw_polygon(self.p_list, self.algorithm)
            for p in item_pixels:
                painter.setPen(self.color)
                painter.drawPoint(*p)
            if self.selected:
                painter.setPen(QColor(255, 0, 0))
                painter.drawRect(self.boundingRect())
        elif self.item_type == 'ellipse':
            item_pixels = alg.draw_ellipse(self.p_list)
            for p in item_pixels:
                painter.setPen(self.color)
                painter.drawPoint(*p)
            if self.selected:
                painter.setPen(QColor(255, 0, 0))
                painter.drawRect(self.boundingRect())
        elif self.item_type == 'curve':
            item_pixels = alg.draw_curve(self.p_list, self.algorithm)
            for p in item_pixels:
                painter.setPen(self.color)
                painter.drawPoint(*p)
            if self.selected:
                painter.setPen(QColor(255, 0, 0))
                painter.drawRect(self.boundingRect())

    def boundingRect(self) -> QRectF:
        if self.item_type == 'line':
            x0, y0 = self.p_list[0]
            x1, y1 = self.p_list[1]
            x = min(x0, x1)
            y = min(y0, y1)
            w = max(x0, x1) - x
            h = max(y0, y1) - y
            return QRectF(x - 1, y - 1, w + 2, h + 2)
        elif self.item_type == 'polygon':
            x0, y0 = self.p_list[0]
            x1, y1 = self.p_list[1]
            for i in range(len(self.p_list)):
                x0 = min(x0, self.p_list[i][0])
                y0 = min(y0, self.p_list[i][1])
                x1 = max(x1, self.p_list[i][0])
                y1 = max(y1, self.p_list[i][1])
            w = x1 - x0
            h = y1 - y0
            return QRectF(x0 - 1, y0 - 1, w + 2, h + 2)
        elif self.item_type == 'ellipse':
            x0, y0 = self.p_list[0]
            x1, y1 = self.p_list[1]
            x = min(x0, x1)
            y = min(y0, y1)
            w = max(x0, x1) - x
            h = max(y0, y1) - y
            return QRectF(x - 1, y - 1, w + 2, h + 2)
        elif self.item_type == 'curve':
            x0, y0 = self.p_list[0]
            x1, y1 = self.p_list[1]
            for i in range(len(self.p_list)):
                x0 = min(x0, self.p_list[i][0])
                y0 = min(y0, self.p_list[i][1])
                x1 = max(x1, self.p_list[i][0])
                y1 = max(y1, self.p_list[i][1])
            w = x1 - x0
            h = y1 - y0
            return QRectF(x0 - 1, y0 - 1, w + 2, h + 2)


class MainWindow(QMainWindow):
    """
    主窗口类
    """
    def __init__(self):
        super().__init__()
        self.item_cnt = 0

        # 使用QListWidget来记录已有的图元，并用于选择图元。注：这是图元选择的简单实现方法，更好的实现是在画布中直接用鼠标选择图元
        self.list_widget = QListWidget(self)
        self.list_widget.setMinimumWidth(200)

        # 使用QGraphicsView作为画布
        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, 600, 600)
        self.canvas_widget = MyCanvas(self.scene, self)
        self.canvas_widget.setFixedSize(600, 600)
        self.canvas_widget.main_window = self
        self.canvas_widget.list_widget = self.list_widget
        self.color = QColor(0, 0, 0)
        self.func_list = ['line_naive_action', 'line_dda_action', 'line_bresenham_action', 'polygon_dda_action',
                          'polygon_bresenham_action', 'ellipse_action','curve_bezier_action','curve_b_spline_action']

        # 设置菜单栏
        menubar = self.menuBar()
        file_menu = menubar.addMenu('文件')
        set_pen_act = file_menu.addAction('设置画笔')
        reset_canvas_act = file_menu.addAction('重置画布')
        exit_act = file_menu.addAction('退出')
        draw_menu = menubar.addMenu('绘制')
        line_menu = draw_menu.addMenu('线段')
        line_naive_act = line_menu.addAction('Naive')
        line_dda_act = line_menu.addAction('DDA')
        line_bresenham_act = line_menu.addAction('Bresenham')
        polygon_menu = draw_menu.addMenu('多边形')
        polygon_dda_act = polygon_menu.addAction('DDA')
        polygon_bresenham_act = polygon_menu.addAction('Bresenham')
        ellipse_act = draw_menu.addAction('椭圆')
        curve_menu = draw_menu.addMenu('曲线')
        curve_bezier_act = curve_menu.addAction('Bezier')
        curve_b_spline_act = curve_menu.addAction('B-spline')
        edit_menu = menubar.addMenu('编辑')
        select_act = edit_menu.addAction('选择')
        translate_act = edit_menu.addAction('平移')
        rotate_act = edit_menu.addAction('旋转')
        scale_act = edit_menu.addAction('缩放')
        clip_menu = edit_menu.addMenu('裁剪')
        clip_cohen_sutherland_act = clip_menu.addAction('Cohen-Sutherland')
        clip_liang_barsky_act = clip_menu.addAction('Liang-Barsky')

        # 连接信号和槽函数
        exit_act.triggered.connect(qApp.quit)
        set_pen_act.triggered.connect(self.set_pen_action)
        line_naive_act.triggered.connect(self.line_naive_action)
        line_dda_act.triggered.connect(self.line_dda_action)
        line_bresenham_act.triggered.connect(self.line_bresenham_action)
        polygon_dda_act.triggered.connect(self.polygon_dda_action)
        polygon_bresenham_act.triggered.connect(self.polygon_bresenham_action)
        ellipse_act.triggered.connect(self.ellipse_action)
        select_act.triggered.connect(self.select_action)
        translate_act.triggered.connect(self.translate_action)
        rotate_act.triggered.connect(self.rotate_action)
        scale_act.triggered.connect(self.scale_action)
        reset_canvas_act.triggered.connect(self.reset_canvas_action)
        clip_cohen_sutherland_act.triggered.connect(self.clip_cohen_sutherland_action)
        clip_liang_barsky_act.triggered.connect(self.clip_liang_barsky_action)
        curve_bezier_act.triggered.connect(self.curve_bezier_action)
        curve_b_spline_act.triggered.connect(self.curve_b_spline_action)
        self.list_widget.currentTextChanged.connect(self.canvas_widget.selection_changed)

        # 设置主窗口的布局
        self.hbox_layout = QHBoxLayout()
        self.hbox_layout.addWidget(self.canvas_widget)
        self.hbox_layout.addWidget(self.list_widget, stretch=1)
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.hbox_layout)
        self.setCentralWidget(self.central_widget)
        self.statusBar().showMessage('空闲')
        self.resize(600, 600)
        self.setWindowTitle('CG Demo')

    def get_id(self):
        _id = str(self.item_cnt)
        self.item_cnt += 1
        #print(self.item_cnt)
        return _id

    def set_pen_action(self):
        #print('input set pen')
        self.color = QColorDialog.getColor()
        if (self.func_state != -1):
            eval('self.' + self.func_list[self.func_state])()

    def line_naive_action(self):
        self.func_state = 0
        self.canvas_widget.start_draw_line('Naive', self.get_id(), self.color)
        self.statusBar().showMessage('Naive算法绘制线段')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def line_dda_action(self):
        self.func_state = 1
        self.canvas_widget.start_draw_line('DDA', self.get_id(), self.color)
        self.statusBar().showMessage('DDA算法绘制线段')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def line_bresenham_action(self):
        self.func_state = 2
        self.canvas_widget.start_draw_line('Bresenham', self.get_id(), self.color)
        self.statusBar().showMessage('Bresenham算法绘制线段')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def polygon_dda_action(self):
        self.func_state = 3
        self.canvas_widget.start_draw_polygon('DDA', self.get_id(), self.color)
        self.statusBar().showMessage('DDA算法绘制多边形')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def polygon_bresenham_action(self):
        self.func_state = 4
        self.canvas_widget.start_draw_polygon('Bresenham', self.get_id(), self.color)
        self.statusBar().showMessage('Bresenham算法绘制多边形')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def ellipse_action(self):
        self.func_state = 5
        self.canvas_widget.start_draw_ellipse(self.get_id(), self.color)
        self.statusBar().showMessage('中点圆生成算法绘制椭圆')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def curve_bezier_action(self):
        self.func_state = 6
        self.canvas_widget.start_draw_curve('Bezier', self.get_id(), self.color)
        self.statusBar().showMessage('Bezier算法绘制曲线')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def curve_b_spline_action(self):
        self.func_state = 7
        self.canvas_widget.start_draw_curve('B-spline', self.get_id(), self.color)
        self.statusBar().showMessage('B_spline算法绘制曲线')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def reset_canvas_action(self):
        self.func_state = -1
        self.canvas_widget.clear_canvas()
        self.statusBar().showMessage('空闲')
        self.scene.clear()
        self.list_widget.clear()
        #self.canvas_widget.list_widget.clear()

    def select_action(self):
        self.func_state = -1
        self.canvas_widget.start_select_item()
        self.list_widget.setCurrentItem(None)

    def translate_action(self):
        self.func_state = -1
        self.canvas_widget.start_translate_item()

    def rotate_action(self):
        self.func_state = -1
        self.canvas_widget.start_rotate_item()

    def scale_action(self):
        self.func_state = -1
        self.canvas_widget.start_scale_item()

    def clip_cohen_sutherland_action(self):
        self.func_state = - 1
        self.canvas_widget.start_clip_item('Cohen-Sutherland')
        self.statusBar().showMessage('Cohen-Sutherland算法裁剪线段')

    def clip_liang_barsky_action(self):
        self.func_state = - 1
        self.canvas_widget.start_clip_item('Liang-Barsky')
        self.statusBar().showMessage('Liang-Barsky算法裁剪线段')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())
