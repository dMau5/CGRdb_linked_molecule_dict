from CGRdb import load_schema
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


def worker(input_queue, output_queue):
    for r in iter(input_queue.get, 'STOP'):
        flag = False
        if r.reactants and r.products:
            for reactant in r.reactants:
                try:
                    reactant.aromatize()
                except:
                    flag = True
                    break
            for product in r.products:
                try:
                    product.aromatize()
                except:
                    flag = True
                    break
            if flag:
                continue
            output_queue.put(r)


if __name__ == '__main__':
    db = load_schema()
    with open('final.rdf', 'r', encoding='utf-8') as f:
        reactions = RDFread(f)
        print('work')
        g = CGRdbDigraph()
        inp = Queue()
        for x in islice(reactions, 100):
            inp.put(x)
        out = Queue()
        for _ in range(12):
            Process(target=worker, args=(inp, out)).start()

        n = 0
        while True:
            sleep(1)
            q1 = out.qsize()
            q2 = inp.qsize()
            if q1:
                # print('do output', q1, q2)
                for _ in range(q1):
                    r = out.get()
                    r.standardize()
                    g.add_node(n, data=[r.meta['source_id'], r.meta['text']])
                    for reactant in r.reactants:
                        g.add_edge(reactant, n)
                    for product in r.products:
                        g.add_edge(n, product)
                    n += 1
                    if not n % 100:
                        print(f'--------{n} done--------')
                        break
                    try:
                        inp.put(next(reactions))
                    except StopIteration:
                        break
                else:
                    continue
                break
            elif not q2:
                # print('do input')
                for e in islice(reactions, 100):
                    inp.put(e)

        for _ in range(12):
            inp.put('STOP')
    with open('biggest_graph.pickle', 'wb') as file:
        pickle.dump(g, file)
        print('URAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
