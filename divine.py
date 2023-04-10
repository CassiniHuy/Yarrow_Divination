import tkinter as tk
import random, time
from typing import List, Tuple


class Divination():
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("蓍草占卜法")
        self.canvas = tk.Canvas(self.root, width=600, height=600)
        self.canvas.pack()
        self.yallows = list()
        self.yaos = list()
        self.txt = None
        self.rounds = 0
        self.moved = list()
        self.taiji = None
        self.ren = None
        self._init_yallows()
        self.canvas.bind("<Button-1>", self._on_click)
        self.root.resizable(False, False)
    
    def _move_yallows(self, yallows: list):
        for yallow in yallows:
            x1, y1, x2, y2 = self.canvas.coords(yallow)
            moved = self.canvas.create_line(60, y1, x2 - x1, y2)
            self.canvas.delete(yallow)
            self.moved.append(moved)
    
    def _revert_divine(self):
        assert len(self.yallows) % 4 == 0
        yao = len(self.yallows) // 4
        self.yaos.append(yao)
        if self.txt:
            self.canvas.delete(self.txt)
        self.txt = self.canvas.create_text(10, 10, text=f'爻：{self.yaos}', anchor="nw")
        for line in self.moved + self.yallows:
            self.canvas.delete(line)
        self._init_yallows()
        self.rounds = 0
        self.moved = list()
        self.taiji = None
        self.ren = None

    def _init_yallows(self, num: int = 50):
        self.yallows = list()
        for _ in range(num):
            x1 = 200 + random.random() * 60
            y1 = 60 + random.random() * 60
            x2 = x1 + random.random() * 60
            y2 = y1 + 200 + random.random() * 60
            line_id = self.canvas.create_line(x1, y1, x2, y2, width=2)
            self.yallows.append(line_id)
        self.left, self.right = list(), list()
    
    def _if_valid(self, x: float, y: float) -> bool:
        coords = [self.canvas.coords(line_id) for line_id in self.yallows]
        x1s = [coord[0] for coord in coords]
        y1s = [coord[1] for coord in coords]
        x2s = [coord[2] for coord in coords]
        y2s = [coord[3] for coord in coords]
        self.min_x = min(min(x1s), min(x2s))
        self.max_x = max(max(x1s), max(x2s))
        self.min_y = min(min(y1s), min(y2s))
        self.max_y = max(max(y1s), max(y2s))
        if x > self.min_x and x < self.max_x:
            if y > self.min_y and y < self.max_y:
                return True
        return False
    
    def _on_click(self, event):
        if self.yallows is None:
            return
        if self.taiji is None:
            self._on_select_yallows(event)
        else:
            if self.left and self.right:
                if self.ren is None:
                    self._on_select_yallows(event)
                else:
                    self._on_yanyi()
            else:
                self._on_split_yallows(event)
            
    def _four_xiang(self, yallows: list) -> Tuple[list, list]:
        n_removed = len(yallows) % 4
        n_removed = 4 if n_removed == 0 else n_removed
        removed = random.sample(yallows, k=n_removed)
        yallows = list(filter(lambda x: x not in removed, yallows))
        return removed, yallows
    
    def _on_split_yallows(self, event):
        x, y = event.x, event.y
        if self._if_valid(x, y) is False or self.yallows is None:
            return
        left, right = list(), list()
        for line_id in self.yallows:
            x1, y1, x2, y2 = self.canvas.coords(line_id)
            self.canvas.delete(line_id)
            if abs(x1 - x) * abs(y1 - y) > abs(x2 - x) * abs(y2 - y):
                line_id = self.canvas.create_line(x1 - 60, y1, x2 - 60, y2, width=2)
                left.append(line_id)
            else:
                line_id = self.canvas.create_line(x1 + 60, y1, x2 + 60, y2, width=2)
                right.append(line_id)
        self.left, self.right = left, right
        self.yallows = self.right
    
    def _on_yanyi(self):
        to_remove_left, yallows_left = self._four_xiang(self.left)
        to_remove_right, yallows_right = self._four_xiang(self.right)
        to_remove, yallows = to_remove_left + to_remove_right, yallows_left + yallows_right
        self.yallows = yallows
        self._move_yallows(to_remove)
        n_remained = len(yallows)
        for line_id in self.yallows:
            self.canvas.delete(line_id)
        self._init_yallows(n_remained)
        self.ren = None
        self.rounds += 1
        if self.rounds == 3:
            self._revert_divine()
    
    def _on_select_yallows(self, event):
        x, y = event.x, event.y
        if self._if_valid(x, y) is False or self.yallows is None:
            return
        dist_f = lambda x0, y0, x1, y1, x2, y2: abs((y2-y1)*x0 - (x2-x1)*y0 + x2*y1 - y2*x1) / ((y2-y1)**2 + (x2-x1)**2)**0.5
        dists = [(yallow, dist_f(x, y, *self.canvas.coords(yallow))) for yallow in self.yallows]
        dists = sorted(dists, key=lambda xy: xy[1])
        yallow = dists[0][0]
        self._move_yallows([yallow])
        self.yallows.remove(yallow)
        if self.taiji is None:
            self.taiji = True
        elif self.ren is None:
            self.ren = True
        else:
             raise RuntimeError(f'Into incorrect branch.')
    
    def run(self):
        self.root.mainloop()

divination = Divination()
divination.run()
