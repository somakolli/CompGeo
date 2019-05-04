#! /usr/bin/env python

from sympy.geometry import Point, Segment
from tkinter import Tk, Canvas


class Vec2D:

    def __init__(self, tuple):
        self.tuple = tuple
        self.x, self.y = tuple

    def __add__(self, other):
        return Vec2D((self.x + other.x, self.y + other.y))

    def __sub__(self, other):
        return Vec2D((self.x - other.x, self.y - other.y))

    def cross(self, other):
        return self.x * other.y - self.y * other.x


class Model:

    def __init__(self):
        self.points = []
        self.segments = []

    def lowest_point(self):
        lowest_point = self.points[0]
        for point in self.points:
            if point[1] < lowest_point[1]:
                lowest_point = point
        return lowest_point

    @staticmethod
    def is_right_of_line(point, segment):
        p, q = segment
        vec_pq = Vec2D(q) - Vec2D(p)
        vec_ppoint = Vec2D(point) - Vec2D(p)
        return vec_pq.cross(vec_ppoint) > 0

    def calc_ch(self):
        self.segments = []
        if len(self.points) < 2:
            return
        if len(self.points) == 2:
            self.segments.append((self.points[0], self.points[1]))
            return
        s = self.lowest_point()
        p = s
        q = self.points[0]
        if q == s:
            q = self.points[1]
        while q != s:
            i = 0
            while q==p:
                i = i+1
                q = self.points[i]
            for point in self.points:
                if self.is_right_of_line(point, (p, q)):
                    q = point
            self.segments.append((p, q))
            p = q

    def clear(self):
        self.points = []
        self.segments = []

    def __str__(self):
        return f"Model: {self.points}, lowest_point: {self.lowest_point()}, ch: {self.segments}"


class View:

    def __init__(self, master, width=800, height=600):
        self.canvas = Canvas(master, width=width, height=height)
        self.canvas.pack()

    def draw_model(self, model, mouse_pos=None):
        self.canvas.delete("all")

        for segment in model.segments:
            self.draw_segment(segment, 'black')
        for point in model.points:
            self.draw_point(point, 'green')


    def draw_segment(self, segment, color):
        p, q = segment
        self.canvas.create_line(*p, *q, fill=color, width=2)

    def draw_point(self, point, color):
        x, y = point
        x1, y1 = (x - 1), (y - 1)
        x2, y2 = (x + 1), (y + 1)
        self.canvas.create_oval(x1, y1, x2, y2, fill=color)


class Controller:

    def __init__(self):
        self.root = Tk()
        self.model = Model()

        self.view = View(self.root)
        self.view.canvas.bind("<Button-1>", self.leftclick)
        self.view.canvas.bind("<Button-3>", self.rightclick)

    def _input_function(f):
        def wrapped(self, event):
            x = self.view.canvas.canvasx(event.x)
            y = self.view.canvas.canvasy(event.y)
            point = (x, y)
            f(self, point)
            self.view.draw_model(self.model)
        return wrapped

    @_input_function
    def leftclick(self, position):
        self.model.segments = []
        self.model.points.append(position)
        self.model.calc_ch()

    @_input_function
    def rightclick(self, position):
        self.model.clear()

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    c = Controller()
    c.run()
