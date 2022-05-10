from bs4 import BeautifulSoup as bs

class osm_parser():

    def __init__(self, file_path):

        with open(file_path, 'r') as f:
            self.data = f.read()
            self.bs_data = bs(self.data, 'xml')

    def set_new_data(self, file_path):
        with open(file_path, 'r') as f:
            self.data = f.read()
            self.bs_data = bs(self.data, 'xml')

    def get_node_lat_lon(self, node_id):
        nodes = self.bs_data.find_all('node')
        for node in nodes:
            if node.get('id') == str(node_id):
                lat = node.get('lat')
                lon = node.get('lon')
                return lat, lon
        raise ValueError('id ist nicht vergeben oder ist falsch')

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
        for h in self.get_highway_dicts():
            if h['id'] == str(building_id):
                lst_node_ids = h['lst_references']
                break
        for node_id in lst_node_ids:
            lat, lon = self.get_node_lat_lon(node_id)
            res.append((lat, lon))
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
            lat, lon = self.get_node_lat_lon(node_id)
            res.append((lat, lon))
        return res

p = osm_parser('data_gerlingen.osm')
print(p.get_highway_nodes(24538510))
dic = p.get_highway_dicts()
print(p.get_highway_dicts())