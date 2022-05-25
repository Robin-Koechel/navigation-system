# Ich habe keine Ahnung, aber ich habe gehört, dass A-Star nicht schlecht sein soll!
import numpy as np
import math

pos_goal = [10, 10]
pos_start = [90, 90]


class node():
    def __init__(self, x, y):
        self.pos = [x, y]
        self.status = 0
    def set_pointer(self, x, y): # points at last node
        self.pointer = [x, y]

    def calc_f(self):
        h = math.sqrt((pos_goal[0]-self.pos[0])**2 + (pos_goal[1]-self.pos[1])**2)
        g = math.sqrt((pos_start[0] - self.pos[0]) ** 2 + (pos_start[1] - self.pos[1]) ** 2)

        return g+h


lst_nodes = []
for i in range(100):
    row = []
    for j in range(100):
        row.append(node(i,j))
        lst_nodes.append(row)


open_lst = [] # has all known nodes -> optimisation: safe as binary  heap not list
closed_lst = []

def get_min_f_open_lst():
    min = open_lst[0]
    for node in open_lst:
        if min.calc_f() < node.calc_f():
            min = node
    return min
def get_successors(x, y):
    lst_successors = []
    lst_successors.append(node(x-1,y-1))
    lst_successors.append(node(x - 1, y))
    lst_successors.append(node(x - 1, y+1))

    lst_successors.append(node(x + 1, y - 1))
    lst_successors.append(node(x + 1, y))
    lst_successors.append(node(x + 1, y + 1))

    lst_successors.append(node(x, y - 1))
    lst_successors.append(node(x, y + 1))
    return lst_successors

def expand_Node(node):
    successors_node = get_successors(node.pos[0], node.pos[1])

    for successor in successors_node:
        in_closed_lst = False
        for i in closed_lst:
            if i == successor:
                in_closed_lst = True
                break
        if in_closed_lst:
            continue
        tentative_g = math.sqrt((pos_start[0] - successor.pos[0]) ** 2 + (pos_start[1] - successor.pos[1]) ** 2)

        for i in open_lst:
            if i == successor:
                if tentative_g < i.calc_f():
                    i.set_pointer(node.pos[0], node.pos[1])
            else:
                successor.set_pointer(node.pos[0], node.pos[1])



open_lst.append(lst_nodes[pos_start[0]][pos_start[1]])

while len(open_lst) > 0:

    current_Node = get_min_f_open_lst()
    open_lst.remove(current_Node)

    if current_Node.pos == pos_goal:
        print("Path found")
        break

    closed_lst.append(current_Node)
    expand_Node(current_Node)

if len(open_lst) < 0:
    print("Path not found")