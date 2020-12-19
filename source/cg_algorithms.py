#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 本文件只允许依赖math库
import math


def draw_line(p_list, algorithm):
    """绘制线段

    :param p_list: (list of list of int: [[x0, y0], [x1, y1]]) 线段的起点和终点坐标
    :param algorithm: (string) 绘制使用的算法，包括'DDA'和'Bresenham'，此处的'Naive'仅作为示例，测试时不会出现
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    x0, y0 = p_list[0]
    x1, y1 = p_list[1]
    if x0 > x1:
        x0, y0, x1, y1 = x1, y1, x0, y0
    result = []
    if algorithm == 'Naive':
        if x0 == x1:
            if y0 > y1:
                y0, y1 = y1, y0
            for y in range(y0, y1 + 1):
                result.append((x0, y))
        else:
            k = (y1 - y0) / (x1 - x0)
            for x in range(x0, x1 + 1):
                result.append((x, int(y0 + k * (x - x0))))
    elif algorithm == 'DDA':
        if x0 == x1:
            if y0 > y1:
                y0, y1 = y1, y0
            for y in range(y0, y1 + 1):
                result.append((x0, y))
        else:
            m = (y1 - y0) / (x1 - x0)
            if ((m <= 1) and (m >= -1)):
                y = y0
                for x in range(x0, x1 + 1):
                    result.append((x, int(y + 0.5)))
                    y = y + m
            else:
                if y0 > y1:
                    x0, y0, x1, y1 = x1, y1, x0, y0
                m = (x1 - x0) / (y1 - y0)
                x = x0
                for y in range(y0, y1 + 1):
                    result.append((int(x + 0.5), y))
                    x = x + m
    elif algorithm == 'Bresenham':
        if x0 == x1:
            if y0 > y1:
                y0, y1 = y1, y0
            for y in range(y0, y1 + 1):
                result.append((x0, y))
        else:
            m = (y1 - y0) / (x1 - x0)
            if ((m <= 1) and (m >= -1)):
                dx = x1 - x0
                dy = y1 - y0
                ind = 1
                if (dy < 0):
                    ind = -1
                    dy = -dy
                pk = 2 * dy - dx
                y = y0
                result.append((x0, y0))
                for k in range(x0, x1):
                    if (pk < 0):
                        pk = pk + 2 * dy
                    else:
                        y = y + ind
                        pk = pk + 2 * dy - 2 * dx
                    result.append((k + 1, y))
            else:
                if y0 > y1:
                    x0, y0, x1, y1 = x1, y1, x0, y0
                m = (x1 - x0) / (y1 - y0)
                dx = x1 - x0
                dy = y1 - y0
                ind = 1
                if (dx < 0):
                    ind = -1
                    dx = -dx
                pk = 2 * dx - dy
                x = x0
                result.append((x0, y0))
                for k in range(y0, y1):
                    if (pk < 0):
                        pk = pk + 2 * dx
                    else:
                        x = x + ind
                        pk = pk + 2 * dx - 2 * dy
                    result.append((x, k + 1))
    return result


def draw_polygon(p_list, algorithm):
    """绘制多边形

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 多边形的顶点坐标列表
    :param algorithm: (string) 绘制使用的算法，包括'DDA'和'Bresenham'
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    result = []
    for i in range(len(p_list)):
        line = draw_line([p_list[i - 1], p_list[i]], algorithm)
        result += line
    return result


def draw_ellipse(p_list):
    """绘制椭圆（采用中点圆生成算法）

    :param p_list: (list of list of int: [[x0, y0], [x1, y1]]) 椭圆的矩形包围框左上角和右下角顶点坐标
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    half_result = []
    x0, y0 = p_list[0]
    x1, y1 = p_list[1]
    xc, yc = int(0.5 * (x0 + x1) + 0.5), int(0.5 * (y0 + y1) + 0.5)
    rx, ry = 0.5 * abs(x0 - x1), 0.5 * abs(y0 - y1)
    pk1 = ry * ry - rx * rx * ry + rx * rx * 0.25
    x, y = 0, int(ry + 0.5)
    half_result.append((x, y))
    while (ry * ry * x < rx * rx *y):
        x = x + 1
        if (pk1 < 0):
            pk1 = pk1 + 2 * ry *ry * x + ry * ry
        else:
            y = y - 1
            pk1 = pk1 + 2 * ry * ry * x - 2 * rx * rx * y + ry * ry
        half_result.append((x, y))

    pk2 = ry * ry *(x + 0.5) *(x + 0.5) + rx * rx * (y - 0.1) * (y - 0.1) - rx * rx * ry * ry
    while (y > 0):
        y = y - 1
        if (pk2 > 0):
            pk2 = pk2 - 2 * rx * rx * y + rx * rx
        else:
            x = x + 1
            pk2 = pk2 + 2 * ry * ry * x - 2 * rx * rx * y + rx + rx
        half_result.append((x, y))
    '''
    pk2 = rx * rx - ry * ry * rx + ry * ry * 0.25
    x, y = int(rx + 0.5), 0
    half_result.append((x, y))
    while (ry * ry * x > rx * rx *y):
        y = y + 1
        if (pk2 < 0):
            pk2 = pk2 + 2 * rx * rx * y + rx * rx
        else:
            x = x - 1
            pk2 = pk2 + 2 * rx * rx * y - 2 * ry * ry * x + rx * rx
        half_result.append((x, y))
    '''
    result = []
    for x,y in half_result:
        result.append((x + xc, y + yc))
        result.append((x + xc, -y + yc))
        result.append((-x + xc, y + yc))
        result.append((-x + xc, -y + yc))
    return result

def draw_curve(p_list, algorithm):
    """绘制曲线

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 曲线的控制点坐标列表
    :param algorithm: (string) 绘制使用的算法，包括'Bezier'和'B-spline'（三次均匀B样条曲线，曲线不必经过首末控制点）
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    def calculate_c(n, m):
        ans = 1
        i = m + 1
        while (i <= n):
            ans = ans * i
            i = i + 1
        for i in range(n - m):
            ans = ans / (i + 1)
        return ans
    def calculate_pu(p_list, u):
        n = len(p_list) - 1
        x, y = 0.0, 0.0
        for i in range(n + 1):
            coef = calculate_c(n, i) * math.pow(u, i) * \
                   math.pow(1 - u, n - i)
            xi, yi = p_list[i]
            x = x + coef * xi
            y = y + coef * yi
        return x, y
    def calculate_b3(i, j , u, k, ran):
        if j == 1:
            if i == k:
                return 1
            else:
                return 0
        b0 = calculate_b3(i, j - 1, u, k, ran)
        b1 = calculate_b3(i + 1, j - 1, u, k, ran)
        ans = ((u - i / ran) / ((i + j - 1) / ran - i / ran)) * b0 + \
              (((i + j) / ran - u)/((i + j) / ran - (i + 1) / ran)) * b1
        return ans

    def calculate_p(p_list, u, k):
        n = len(p_list) - 1
        x, y = 0.0, 0.0
        for i in range(n + 1):
            coef = calculate_b3(i, 4, u, k, n + 4)
            xi, yi = p_list[i]
            x = x + coef * xi
            y = y + coef * yi
        return x, y

    dot_list = []
    if algorithm == 'Bezier':
        precision = 100
        for i in range(precision + 1):
            u = i * 1.0 / precision
            x, y = calculate_pu(p_list, u)
            dot_list.append((int(x), int(y)))
    elif algorithm == 'B-spline':
        n = len(p_list) -1
        k = 4
        ran = n + k
        precision = 100
        for i in range(n + 1):
            #print('{} {}'.format(i, k-1))
            if i >= k - 1:
                for j in range(precision + 1):
                    #print('add dot')
                    u = i * 1.0 / ran + j * 1.0 / precision / ran
                    x, y = calculate_p(p_list, u, i)
                    dot_list.append((int(x), int(y)))
    #print('curve part:')
    #print(p_list)
    #print(dot_list)
    result = []
    for i in range(len(dot_list)):
        if i != 0:
            line = draw_line([dot_list[i - 1], dot_list[i]], 'DDA')
            result += line
    return result

def translate(p_list, dx, dy):
    """平移变换

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param dx: (int) 水平方向平移量
    :param dy: (int) 垂直方向平移量
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    result = []
    for x, y in p_list:
        result.append((x + dx, y + dy))
    return result

def rotate(p_list, xc, yc, r):
    """旋转变换（除椭圆外）

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param x: (int) 旋转中心x坐标
    :param y: (int) 旋转中心y坐标
    :param r: (int) 顺时针旋转角度（°）
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """

    print('start rotate')
    '''
    l0 = math.sqrt(x0 * x0 + y0 * y0)
    l1 = math.sqrt(x1 * x1 + y1 * y1)
    if (l0 == 0 or l1 == 0):
        return p_list
    print('rotating')
    cosa = (x0 * x1 + y0 * y1) * 1.0 / l0 / l1
    print(cosa)
    r = math.acos(cosa)
    if (x0 * y1 - x1 * y0 < 0):
        r = 2 * math.pi - r
    '''
    result = []
    rad = r * math.pi / 180
    for x, y in p_list:
        result.append((int(xc + (x - xc) * math.cos(rad) - (y - yc) * math.sin(rad)),
                       int(yc + (x - xc) * math.sin(rad) + (y - yc) * math.cos(rad))))
    return result

def scale(p_list, xc, yc, s):
    """缩放变换

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param x: (int) 缩放中心x坐标
    :param y: (int) 缩放中心y坐标
    :param s: (float) 缩放倍数
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    result = []
    for x, y in p_list:
        result.append((int(x * s + xc * (1 - s)),
                       int(y * s + yc * (1 - s))))
    return result

def clip(p_list, x_min, y_min, x_max, y_max, algorithm):
    """线段裁剪

    :param p_list: (list of list of int: [[x0, y0], [x1, y1]]) 线段的起点和终点坐标
    :param x_min: 裁剪窗口左上角x坐标
    :param y_min: 裁剪窗口左上角y坐标
    :param x_max: 裁剪窗口右下角x坐标
    :param y_max: 裁剪窗口右下角y坐标
    :param algorithm: (string) 使用的裁剪算法，包括'Cohen-Sutherland'和'Liang-Barsky'
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1]]) 裁剪后线段的起点和终点坐标
    """
    print('do clip line operation:')
    x0, y0 = p_list[0]
    x1, y1 = p_list[1]
    result = []
    def sgn(x):
        if x > 0:
            return 1
        else:
            return 0
    if algorithm == 'Cohen-Sutherland':
        code0 = sgn(x_min - x0)
        code1 = sgn(x_min - x1)
        code0 = (code0 << 1) | sgn(x0 - x_max)
        code1 = (code1 << 1) | sgn(x1 - x_max)
        code0 = (code0 << 1) | sgn(y_min - y0)
        code1 = (code1 << 1) | sgn(y_min - y1)
        code0 = (code0 << 1) | sgn(y0 - y_max)
        code1 = (code1 << 1) | sgn(y1 - y_max)
        if (code0 == 0 and code1 == 0):
            return [[x0, y0], [x1, y1]]
        if ((code0 & code1) != 0):
            return None
        if (y0 == y1):
            if ((code0 & 8) == 8):
                x0 = x_min
            if ((code0 & 4) == 4):
                x0 = x_max
            if ((code1 & 8) == 8):
                x1 = x_min
            if ((code1 & 4) == 4):
                x1 = x_max
            return [[x0, y0], [x1, y1]]
        if (x0 == x1):
            if ((code0 & 2) == 2):
                y0 = y_min
            if ((code0 & 1) == 1):
                y0 = y_max
            if ((code1 & 2) == 2):
                y1 = y_min
            if ((code1 & 1) == 1):
                y1 = y_max
            return [[x0, y0], [x1, y1]]
        m = (y0 - y1) * 1.0 / (x0 - x1)
        def change_xy_prime(x, y, m, x_min, y_min, x_max, y_max):
            if (x < x_min):
                y = y + m * (x_min - x)
                x = x_min
            if (x > x_max):
                y = y + m * (x_max - x)
                x = x_max
            if (y > y_max):
                x = x + (y_max - y) / m
                y = y_max
            if (y < y_min):
                x = x + (y_min - y) / m
                y = y_min
            return int(x), int(y)
        x0, y0 = change_xy_prime(x0, y0, m, x_min, y_min, x_max, y_max)
        x1, y1 = change_xy_prime(x1, y1, m, x_min, y_min, x_max, y_max)
        return [[x0, y0], [x1, y1]]
    elif algorithm == 'Liang-Barsky':
        u0, u1 = 0.0, 1.0
        p = [0, 0, 0, 0]
        q = [0, 0, 0, 0]
        p[0] = x0 - x1
        p[1] = x1 - x0
        p[2] = y0 - y1
        p[3] = y1 - y0
        q[0] = x0 - x_min
        q[1] = x_max - x0
        q[2] = y0 - y_min
        q[3] = y_max - y0
        for i in range(4):
            pk, qk = p[i], q[i]
            #print('{}   {}'.format(pk, qk))
            if pk == 0:
                if qk < 0 :
                    return None
                else:
                    return [[x0, y0], [x1, y1]]
            u = qk / pk
            #print(u)
            if pk < 0:
                u0 = max(u0, u)
            else:
                u1 = min(u1, u)
            #print('{}   {}'.format(u0, u1))
            if u0 > u1:
                return None
        result.append((int(x0 + u0 * (x1 - x0)), int(y0 + u0 * (y1 - y0))))
        result.append((int(x0 + u1 * (x1 - x0)), int(y0 + u1 * (y1 - y0))))
        #print(p_list)
        #print(result)
        #print('{} {} {} {}'.format(x_min, x_max, y_min, y_max))
    return result
