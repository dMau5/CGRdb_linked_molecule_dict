import networkx as nx
from redict import CGRdbDict
from CGRdb import load_schema
db = load_schema('schema', user='user', password='pass', host='host', database='postgres')


class CGRdbDigraph(nx.DiGraph):
    CGRdbDict.attached = db
    node_dict_factory = CGRdbDict
    adjlist_outer_dict_factory = CGRdbDict
    adjlist_inner_dict_factory = CGRdbDict
