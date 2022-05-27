import math
open_lst = []
closed_lst = []

start_point = () # lat, lon
goal_point = () # lat, lon

open_lst.append(start_point)

def calc_f_value(lon, lat):
    v_s_x = (lon - start_point[0], lat - start_point[1])
    v_g_x = (lon - goal_point[0], lat - goal_point[1])
    g = math.sqrt(v_s_x[0]**2 + v_s_x[1]**2)
    h =math.sqrt(v_g_x[0]**2 + v_g_x[1]**2)
    return g + h # f = g + h

def expand_node(lon, lat):


while len(open_lst) > 0:
    # current node is the one with min f-value
    current_node = (open_lst[0])
    for p in open_lst:
        if calc_f_value(p[0], p[1]) < calc_f_value(current_node[0], current_node[1]):
            current_node = p
            open_lst.remove(p)
    closed_lst.append(current_node)
    if current_node == goal_point:
        print("goal found")


