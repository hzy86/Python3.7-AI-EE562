"""
Created on Thu 10/25/2018  0:48:55.02

@author: Ziyi Huang

EE 562 HW2 - A* search
"""
import math
import heapq

# class for states in this problem
class state:
    """
    a state consisted of a coordinate, g, h, f values, a list of valid successors
    and a parent state
    """
    def __init__(self, state):
        self.state = state
        self.g, self.h, self.f = 0, 0, 0
        self.successors = []
        self.parent = None

    def __cmp__(self, other):
        """ rank by f value """
        return cmp(self.f, other.f)

    def cost(self, other):
        """ return the cost of moving to point other """
        return math.sqrt((self.state[0] - other[0])**2 + (self.state[1] - other[1])**2)

    def update_f(self):
        """ recalculate its f """
        self.f = self.g + self.h

# class to search for the best path from a data file
class solution:
    result = []
    def __init__(self):
        self.init_state, self.goal_state = (0, 0), (0, 0)
        self.finite_set, self.paths = [], []
        self.obstacles, self.open, self.closed = [], [], []

    def construct(self, filename):
        """
        construct the start state, the goal state and obstacles given the name
        of the text file
        """
        f = open(filename)

        # initialize the initial state and the goal state
        coords = f.readline().split()
        self.init_state = (float(coords[0]), float(coords[1]))

        coords = f.readline().split()
        self.goal_state = (float(coords[0]), float(coords[1]))

        # group points by obstacles and points
        ob_cnt = f.readline()
        for i in range(int(ob_cnt)):
            obs = f.readline()
            obs_coords = obs.split()
            self.obstacles.append([])
            it = iter(obs_coords)
            for x in it:
                s = (float(x), float(next(it)))
                self.obstacles[-1].append(s)
                self.finite_set.append(s)

        f.close()

        # find out valid paths and store them in self.paths
        self.valid_path()

        for obs in self.obstacles:
            print obs

    def valid_path(self):
        """ generate valid paths within the point set"""
        for p1 in self.finite_set:
            for p2 in self.finite_set:
                if p1 == p2: continue

                if self.obs_valid(p1, p2) and not (p1, p2) in self.paths:
                    self.paths.append((p1, p2))

    def line_intersect(self, a, b, c, d):
        """ determine if two line intersect using Cramer's Rule"""
        A1 = (a[1] - b[1])
        B1 = (b[0] - a[0])
        C1 = (a[0]*b[1] - b[0]*a[1])

        A2 = (c[1] - d[1])
        B2 = (d[0] - c[0])
        C2 = (c[0]*d[1] - d[0]*c[1])

        D  = A1 * B2 - A2 * B1
        Dx = -C1 * B2 + B1 * C2
        Dy = -A1 * C2 + C1 * A2
        if D != 0:
            x = Dx / D
            y = Dy / D
            if self.on_segment(x, y, a, b) and self.on_segment(x, y, c, d):
                return True
            return False
        else:
            # parallel
            return False

    def on_segment(self, x, y, a, b):
        """ determine if point (x, y) is on line ab but not overlap a or b """
        xa, xb, ya, yb = a[0], b[0], a[1], b[1]
        return x >= min(xa, xb) and x <= max(xa, xb) and y >= min(ya, yb) and y <= max(ya, yb) \
                and not (y == ya and x == xa) and not (y == yb and x == xb)
    # def ccw(self, a, b, c):
    #     """ determine if a, b, c are listed in counterclockwise order """
    #     return (c[1]-a[1])*(b[0]-a[0]) > (b[1]-a[1])*(c[0]-a[0])
    #
    # def line_intersect(self, a, b, c, d):
    #     """ return if line ab intersects line cd """
    #     return self.ccw(a, c, d) != self.ccw(b, c, d) and self.ccw(a, b, c) != self.ccw(a, b, d)

    def rect_valid(self, a, b, rect):
        """
        return if line ab intersects with the rectangle formed by the 4 vertices
        in rect
        """
        return not self.line_intersect(a, b, rect[0], rect[1]) and \
                not self.line_intersect(a, b, rect[1], rect[2]) and \
                not self.line_intersect(a, b, rect[2], rect[3]) and \
                not self.line_intersect(a, b, rect[3], rect[0]) and \
                not self.line_intersect(a, b, rect[0], rect[2]) and \
                not self.line_intersect(a, b, rect[1], rect[3])

    def obs_valid(self, a, b):
        """ return if ab intersects with any obstacle """
        for o in self.obstacles:
            if not self.rect_valid(a, b, o):
                return False
        return True

    def successors(self, best):
        """ find valid successors for the node """
        succ = []
        for vertex in self.finite_set:
            if best == vertex: continue

            if (best, vertex) in self.paths:
                succ.append(vertex)
        return succ

    def onList(self, node, list):
        """
        return a node on the list that has the same state as node,
        return null if there is none
        """
        for old in list:
            if node.state == old.state: return old
        return

    def run(self):
        """ run the A* search """
        init_node = state(self.init_state)
        init_node.h = init_node.cost(self.goal_state)
        init_node.update_f()
        heapq.heappush(self.open, init_node)

        while self.open:
            best = heapq.heappop(self.open)
            if best.state == self.goal_state:
                while best:
                    self.result.insert(0, best)
                    best = best.parent
                for r in self.result: print r.state, "[{} {} {}]".format(r.g, r.h, r.f)
                return
            self.closed.append(best)
            best_succ = self.successors(best.state)

            for s in best_succ:
                node = state(s)

                if self.onList(node, self.closed): continue

                node.parent = best
                node.g, node.h = node.cost(node.parent.state) + node.parent.g, node.cost(self.goal_state)
                node.update_f()

                old = self.onList(node, self.open)
                if old:
                    if old.g > node.g:
                        old.g = node.g
                        old.parent = best
                        old.update_f()
                        heapq.heapify(self.open)
                    continue

                heapq.heappush(self.open, node)

if __name__ == '__main__':
    sol = solution()
    sol.construct("data2.txt")
    sol.run()
