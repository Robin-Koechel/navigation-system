from bs4 import BeautifulSoup as bs
import math

class osm_parser():

    def __init__(self, file_path):

        with open(file_path, 'r', encoding="utf8") as f:
            self.data = f.read()
            self.bs_data = bs(self.data, 'xml')

    def set_new_data(self, file_path):
        with open(file_path, 'r') as f:
            self.data = f.read()
            self.bs_data = bs(self.data, 'xml')

    def get_Lat_Lon_Box(self):
        b_bound = self.bs_data.find('bounds')
        min_lat = float(b_bound.get('minlat'))
        min_lon = float(b_bound.get('minlon'))
        max_lat = float(b_bound.get('maxlat'))
        max_lon = float(b_bound.get('maxlon'))
        BBox = (min_lon, max_lon,
                min_lat, max_lat)
        return BBox

    def get_lst_node_ids(self):
        lst_ids = []
        nodes = self.bs_data.find_all('node')
        for node in nodes:
            lst_ids.append(node.get('id'))
        return lst_ids

    def get_node_lat_lon_by_id(self, node_id):
        nodes = self.bs_data.find_all('node')
        for node in nodes:
            if node.get('id') == str(node_id):
                lat = node.get('lat')
                lon = node.get('lon')
                return float(lat), float(lon)
        raise ValueError('id ist nicht vergeben oder ist falsch')

    def get_node_id_by_lat_lon(self, lat, lon):
        nodes = self.bs_data.find_all('node')
        for node in nodes:
            if node.get('lat') == lat:
                if node.get('lon') == lon:
                    return node.get('id')

    def get_nodes_neighbours(self, node_id):
        lst_highway_dics = self.get_highway_dicts()
        lst_neighbours = []
        for highway in lst_highway_dics:
            nodes = highway.get('lst_references')
            for idx, node in enumerate(nodes):
                if int(node) == node_id:
                    try:
                        lst_neighbours.append(nodes[idx-1])
                    except:
                        pass
                    try:
                        lst_neighbours.append(nodes[idx+1])
                    except:
                        pass
        lst_neighbours = list(dict.fromkeys(lst_neighbours))
        return lst_neighbours


    def get_nodes_nearest_neighbour(self, node_id, number_of_neighbours):# but only highways
        lat1, lon1 = self.get_node_lat_lon_by_id(node_id)
        lst_nodes = []

        for highway in p.get_highway_dicts():
            for n in highway.get('lst_references'):
                lst_nodes.append(n)
        list(dict.fromkeys(lst_nodes)) # remove dublicates

        node_id_distance = {}
        lst_neighbour_nodes_ids = []
        for node in lst_nodes: # node = node id
            lat2, lon2 = self.get_node_lat_lon_by_id(node)
            distance = self.get_distance_lat_lon_in_km(lat1, lon1, lat2, lon2)
            if distance != 0:
                node_id_distance.update({node:distance})
        node_id_distance = {k: v for k, v in sorted(node_id_distance.items(), key=lambda item: item[1])} # sort dict
        print(node_id_distance)
        for k in node_id_distance:
            if len(lst_neighbour_nodes_ids) < number_of_neighbours:
                lst_neighbour_nodes_ids.append(k)
            else:
                break
        return lst_neighbour_nodes_ids

    def get_distance_lat_lon_in_km(self, lat1, lon1, lat2, lon2):
        # https://www.movable-type.co.uk/scripts/latlong.html
        radius = 6371 #radius of earth
        delta_lat = self.degree_to_rad(lat2-lat1)
        delta_lon = self.degree_to_rad(lon2 - lon1)

        a = math.sin(delta_lat/2) * math.sin(delta_lat/2)+\
            math.cos(self.degree_to_rad(lat1)) * math.cos(self.degree_to_rad(lat2))*\
            math.sin(delta_lon/2) * math.sin(delta_lon/2)

        c = 2 *math.atan2(math.sqrt(a), math.sqrt(1-a))
        d = radius * c # in km
        return d
    def degree_to_rad(self,deg):
        return deg * math.pi/180

    def get_Building_dicts(self):
        st_Building_dicts = []

        ways = self.bs_data.find_all('way')
        lst_Building_tags = []
        for way in ways:
            tags_in_way = way.find_all('tag')
            for tag in tags_in_way:
                if tag.get('k') == "building":
                    lst_Building_tags.append(way)
        for building in lst_Building_tags:
            dict = {}

            id = building.get('id')
            dict['id'] = id

            lst_refs = []
            nds = building.find_all('nd')
            for nd in nds:
                ref = nd.get('ref')
                lst_refs.append(ref)
            dict["lst_references"] = lst_refs

            tags = building.find_all('tag')
            for tag in tags:
                key = tag.get('k')
                value = tag.get('v')
                dict[key] = value
            st_Building_dicts.append(dict)

        return st_Building_dicts

    def get_Building_nodes(self, building_id):
        lst_node_ids = []

        res = []
        for h in self.get_Building_dicts():
            if h['id'] == str(building_id):
                lst_node_ids = h['lst_references']
                break
        for node_id in lst_node_ids:
            lat, lon = self.get_node_lat_lon_by_id(node_id)
            res.append((float(lat), float(lon)))
        return res

    def get_highway_dicts(self):
        lst_highway_dicts = []

        ways = self.bs_data.find_all('way')
        lst_highway_tags = []
        for way in ways:
            tags_in_way = way.find_all('tag')
            for tag in tags_in_way:
                if tag.get('k') == "zone:traffic":
                    lst_highway_tags.append(way)

        for highway in lst_highway_tags:
            dict = {}

            id = highway.get('id')
            dict['id'] = id

            lst_refs = []
            nds = highway.find_all('nd')
            for nd in nds:
                ref = nd.get('ref')
                lst_refs.append(ref)
            dict["lst_references"] = lst_refs

            tags = highway.find_all('tag')
            for tag in tags:
                key = tag.get('k')
                value = tag.get('v')
                dict[key] = value
            lst_highway_dicts.append(dict)

        return lst_highway_dicts

    def get_highway_nodes(self, highway_id):
        lst_node_ids = []

        res = []
        for h in self.get_highway_dicts():
            if h['id'] == str(highway_id):
                lst_node_ids = h['lst_references']
                break
        for node_id in lst_node_ids:
            lat, lon = self.get_node_lat_lon_by_id(node_id)
            res.append((float(lat), float(lon)))
        return res

if __name__ == "__main__":
    p = osm_parser('data_gerlingen.osm')
    #print(p.get_highway_nodes(592135167))
    #dic = p.get_highway_dicts()
    #print(p.get_highway_dicts())
    nnn = p.get_nodes_neighbours(152292474)
    print(p.get_node_lat_lon_by_id(152292474), "\n")
    for n in nnn:
        print(p.get_node_lat_lon_by_id(n))
