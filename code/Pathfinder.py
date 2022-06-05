import math
from tqdm import tqdm
from parse_osm_files import osm_parser
parser = osm_parser('data_gerlingen.osm')
node_pointers = {} #ids
open_lst = []
closed_lst = []

start_point = 1169039074 # id
goal_point = 1169040511 # id

open_lst.append(start_point)

def calc_f_value(lat, lon):
    s_lat_lon = parser.get_node_lat_lon_by_id(start_point)
    g_lat_lon = parser.get_node_lat_lon_by_id(goal_point)

    v_s_x = (lat - s_lat_lon[0], lon - s_lat_lon[1])
    v_g_x = (lat - g_lat_lon[0], lon - g_lat_lon[1])
    g = math.sqrt(v_s_x[0]**2 + v_s_x[1]**2)
    h = math.sqrt(v_g_x[0]**2 + v_g_x[1]**2)
    return g + h # f = g + h

def expand_node(id):
    open_lst_canidate = []
    for node in parser.get_nodes_neighbours(id):
        open_lst_canidate.append(node)

    for node_id in open_lst:
        in_closed_list = False
        for c in closed_lst:
            if node_id == c:
                in_closed_list = True
        if not in_closed_list:
            open_lst.append(node_id)
            node_pointers.update({node_id:id})


# current node is the one with min f-value
current_node = open_lst[0]
while len(open_lst) > 0:
    current_node_lat_lon = parser.get_node_lat_lon_by_id(current_node)

    for p in open_lst:
        p_lat_lon = parser.get_node_lat_lon_by_id(p)
        if calc_f_value(p_lat_lon[0], p_lat_lon[1]) < calc_f_value(current_node_lat_lon[0], current_node_lat_lon[1]):
            current_node = p
            open_lst.remove(p)
    closed_lst.append(current_node)
    expand_node(current_node)

    if current_node == goal_point:
        print("goal found")
        id = goal_point
        while id != start_point:
            print(node_pointers.get(id))
            id = node_pointers.get(id)

