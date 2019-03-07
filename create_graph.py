from CGRdb import load_schema, Molecule
from CGRdbUser import User
from pony.orm import db_session
from CGRtools.files import RDFread
from digraph import CGRdbDigraph
import pickle
from multiprocessing import Process, Queue
from time import sleep
from itertools import islice
import logging


logging.basicConfig(level=logging.ERROR)


# with open('biggest_graph.pickle', 'rb') as f:
#     db = load_schema('sandbox', user='postgres', password='jyvt0n3', host='localhost', database='postgres')
#     g = pickle.load(f)
#     q = 5


def worker(input_queue):
    for r in iter(input_queue.get, 'STOP'):
        try:
            r.standardize()
            with db_session:
                for reactant in r.reactants:
                    # if isinstance(reactant, MoleculeContainer):
                    if not Molecule.structure_exists(reactant):
                        Molecule(reactant, User[1])
                    # g.add_edge(reactant, n)
                for product in r.products:
                    if not Molecule.structure_exists(product):
                        Molecule(product, User[1])
        except:
            continue


if __name__ == '__main__':
    db = load_schema('profile')
    with open('final.rdf', 'r', encoding='utf-8') as f:
        reactions = RDFread(f)
        print('work')
        # g = CGRdbDigraph()
        inp = Queue()
        for x in reactions:
            inp.put(x)
        for _ in range(12):
            Process(target=worker, args=inp).start()
        for _ in range(12):
            inp.put('STOP')
        # n = 0
        # while True:
        #     sleep(1)
        #     q1 = inp.qsize()
        #     if q1:
        #         # print('do output', q1, q2)
        #         for _ in range(q1):
        #             r = inp.get()
        #             # g.add_node(n, data=[r.meta['source_id'], r.meta['text']])
        #             for reactant in r.reactants:
        #                 # if isinstance(reactant, MoleculeContainer):
        #                 if not Molecule.structure_exists(reactant):
        #                     Molecule(reactant, User[1])
        #                 # g.add_edge(reactant, n)
        #             for product in r.products:
        #                 if not Molecule.structure_exists(product):
        #                     Molecule(product, User[1])
        #                 # g.add_edge(n, product)
        #             n += 1
        #             if not n % 100:
        #                 print(f'--------{n} done--------')
        #                 # break
        #             try:
        #                 inp.put(next(reactions))
        #             except StopIteration:
        #                 break
        #         else:
        #             continue
        #         break
        #     # elif not q2:
        #     #     # print('do input')
        #     #     for e in islice(reactions, 100):
        #     #         inp.put(e)
        #

    # with open('biggest_graph.pickle', 'wb') as file:
    #     pickle.dump(g, file)
    #     print('URAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
