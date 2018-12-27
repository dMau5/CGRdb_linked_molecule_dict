from networkx import Digraph
from redict import CGRdbDict


class CGRdbDigraph(DiGraph):
    node_dict_factory = CGRdbDict
    adjlist_outer_dict_factory = CGRdbDict
    adjlist_inner_dict_factory = CGRdbDict
