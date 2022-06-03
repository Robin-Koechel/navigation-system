import math
from tqdm import tqdm
from parse_osm_files import osm_parser
parser = osm_parser('data_gerlingen.osm')
node_pointers = {} #ids
open_lst = []
closed_lst = []

start_point = parser.get_node_lat_lon_by_id(1169039074) # lat, lon
goal_point = parser.get_node_lat_lon_by_id(1169040511) # lat, lon

open_lst.append(start_point)

def calc_f_value(lat, lon):
    v_s_x = (lat - start_point[0], lon - start_point[1])
    v_g_x = (lat - goal_point[0], lon - goal_point[1])
    g = math.sqrt(v_s_x[0]**2 + v_s_x[1]**2)
    h =math.sqrt(v_g_x[0]**2 + v_g_x[1]**2)
    return g + h # f = g + h

def expand_node(lat, lon):
    lst_dists = [1000, 1000, 1000, 1000]
    lst_closest_nodes_ids = [0, 0, 0, 0]

    lst_nodes = parser.get_lst_node_ids()
    for node_id in lst_nodes:
        n_lat, n_lon = parser.get_node_lat_lon_by_id(node_id)
        v_s_x = (lat - n_lat, lon - n_lon)
        amount_v_s_x = math.sqrt(v_s_x[0]**2 + v_s_x[1]**2)

        if amount_v_s_x <= lst_dists[len(lst_dists)-1]:
            lst_dists[len(lst_dists) - 1] = amount_v_s_x
            lst_closest_nodes_ids[len(lst_dists)-1] = node_id
        elif amount_v_s_x <= lst_dists[len(lst_dists)-2]:
            lst_dists[len(lst_dists) - 2] = amount_v_s_x
            lst_closest_nodes_ids[len(lst_dists) - 2] = node_id
        elif amount_v_s_x <= lst_dists[len(lst_dists)-3]:
            lst_dists[len(lst_dists) - 3] = amount_v_s_x
            lst_closest_nodes_ids[len(lst_dists) - 3] = node_id
        elif amount_v_s_x <= lst_dists[len(lst_dists) - 4]:
            lst_dists[len(lst_dists) - 4] = amount_v_s_x
            lst_closest_nodes_ids[len(lst_dists) - 4] = node_id

    for node_id in lst_closest_nodes_ids:
        cords = (parser.get_node_lat_lon_by_id(node_id))
        in_closed_list = False
        for c in closed_lst:
            if cords == c:
                in_closed_list = True
        if not in_closed_list:
            open_lst.append(cords)
            node_pointers.update({node_id:parser.get_node_id_by_lat_lon(cords)})



while len(open_lst) > 0:
    # current node is the one with min f-value
    current_node = (open_lst[0])
    for p in open_lst:
        if calc_f_value(p[0], p[1]) < calc_f_value(current_node[0], current_node[1]):
            current_node = p
            open_lst.remove(p)
    closed_lst.append(current_node)
    print(current_node)
    if current_node == goal_point:
        print("goal found")


