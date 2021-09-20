# based on open-source implementation:
# https://xor0110.wordpress.com/2011/05/09/dlx-in-python-with-actual-pointers/
class Node:
    def __init__(self):
        self.left = self
        self.right = self
        self.up = self
        self.down = self
        self.column = self

    def get_pointer(self, mode = None):
        if mode == None: return self.column
        elif mode == 'left': return self.left
        elif mode == 'right': return self.right
        elif mode == 'up': return self.up
        elif mode == 'down': return self.down

    def left_sweep(self):
        x = self.left
        while x != self:
            yield x; x = x.left
        return None

    def right_sweep(self):
        x = self.right
        while x != self:
            yield x; x = x.right
        return None

    def down_sweep(self):
        x = self.down
        while x != self:
            yield x; x = x.down
        return None

    def up_sweep(self):
        x = self.up
        while x != self:
            yield x; x = x.up
        return None

class DLX:
    def __init__(self, columns, rows):
        self.h = Node()
        self.hdic = dict()
        self.kcount = [0]

        for column in columns:
            self.h.left.right = Node()
            self.h.left.right.right = self.h
            self.h.left.right.left = self.h.left
            self.h.left = self.h.left.right

            self.h.left.column = column
            self.h.left.size = 0
            self.hdic[column] = self.h.left

        for row in rows:
            last = None
            for rlabel in row:
                element = Node()

                element.column = self.hdic[rlabel]
                element.column.size += 1

                element.column.up.down = element
                element.up = element.column.up
                element.down = element.column
                element.column.up = element

                if last:
                    element.left = last
                    element.right = last.right
                    last.right.left = element
                    last.right = element
                last = element

    def cover(self, column: Node):
        column.right.left = column.left
        column.left.right = column.right
        for i in column.down_sweep():
            for j in i.right_sweep():
                j.down.up = j.up
                j.up.down = j.down
                j.column.size -= 1
        return self

    def uncover(self, column: Node):
        for i in column.up_sweep():
            for j in i.left_sweep():
                j.column.size += 1
                j.down.up = j
                j.up.down = j
        column.right.left = column
        column.left.right = column
        return self

    def search(self, k: int = 0, o: list = None):
        c = Node()
        if o is None: o = []

        if len(self.kcount) <= k: self.kcount.append(0)
        self.kcount[k] += 1

        if self.h.right == self.h:
            yield o
            return

        import numpy as np
        size = np.inf

        for column in self.h.right_sweep():
            if column.size < size:
                size = column.size
                c = column

        self.cover(c)
        for r in c.down_sweep():
            o_k = r
            for j in r.right_sweep():
                self.cover(j.column)
            yield from self.search(k = k + 1, o = o+[o_k])
            for j in list(r.left_sweep()): self.uncover(j.column)
        self.uncover(c)
        return self

    def get_row_labels(self, row: Node, sort: bool = True, key = str, reverse: bool = False):
        columns = [row.column.column]
        sweep = list(row.right_sweep())
        for r in sweep: columns.append(r.column.column)
        if sort: columns = sorted(columns, key = key, reverse = reverse)
        return columns

    def generate_solutions(self, **kw):
        self.kcount = [0]

        for solution in self.search():
            yield [self.get_row_labels(s, **kw) for s in solution]

    def __call__(self, return_solutions: bool = True, **kw) -> bool:
        self.kcount = [0]
        solutions = []
        for solution in self.search():
            solutions.append([self.get_row_labels(s, **kw) for s in solution])
            if not return_solutions:
                return True #one solution is enough to prove the existence
        if return_solutions: return solutions
        return False
