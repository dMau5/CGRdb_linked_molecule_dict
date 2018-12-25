import networkx as nx
from redict import CGRdbDict


class CGRdbDigraph(nx.DiGraph):
    node_dict_factory = CGRdbDict
    adjlist_outer_dict_factory = CGRdbDict
    adjlist_inner_dict_factory = CGRdbDict