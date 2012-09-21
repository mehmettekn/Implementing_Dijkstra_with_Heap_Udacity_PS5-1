""" Utility Functions"""

import time
from random import randint
import heapq

""" priority_dict class was used to  implement heaps efficiently. The class makes it
possible to update the dictionary key values in constant time. The class was taken from
the url given below."""

## {{{ http://code.activestate.com/recipes/522995/ (r1)
from heapq import heapify, heappush, heappop

class priority_dict(dict):
    """Dictionary that can be used as a priority queue.

    Keys of the dictionary are items to be put into the queue, and values
    are their respective priorities. All dictionary methods work as expected.
    The advantage over a standard heapq-based priority queue is
    that priorities of items can be efficiently updated (amortized O(1))
    using code as 'thedict[item] = new_priority.'

    The 'smallest' method can be used to return the object with lowest
    priority, and 'pop_smallest' also removes it.

    The 'sorted_iter' method provides a destructive sorted iterator.
    """
    
    def __init__(self, *args, **kwargs):
        super(priority_dict, self).__init__(*args, **kwargs)
        self._rebuild_heap()

    def _rebuild_heap(self):
        self._heap = [(v, k) for k, v in self.iteritems()]
        heapify(self._heap)

    def smallest(self):
        """Return the item with the lowest priority.

        Raises IndexError if the object is empty.
        """
        
        heap = self._heap
        v, k = heap[0]
        while k not in self or self[k] != v:
            heappop(heap)
            v, k = heap[0]
        return k

    def pop_smallest(self):
        """Return the item with the lowest priority and remove it.

        Raises IndexError if the object is empty.
        """
        
        heap = self._heap
        v, k = heappop(heap)
        while k not in self or self[k] != v:
            v, k = heappop(heap)
        del self[k]
        return k

    def __setitem__(self, key, val):
        # We are not going to remove the previous value from the heap,
        # since this would have a cost O(n).
        
        super(priority_dict, self).__setitem__(key, val)
        
        if len(self._heap) < 2 * len(self):
            heappush(self._heap, (val, key))
        else:
            # When the heap grows larger than 2 * len(self), we rebuild it
            # from scratch to avoid wasting too much memory.
            self._rebuild_heap()

    def setdefault(self, key, val):
        if key not in self:
            self[key] = val
            return val
        return self[key]

    def update(self, *args, **kwargs):
        # Reimplementing dict.update is tricky -- see e.g.
        # http://mail.python.org/pipermail/python-ideas/2007-May/000744.html
        # We just rebuild the heap from scratch after passing to super.
        
        super(priority_dict, self).update(*args, **kwargs)
        self._rebuild_heap()

    def sorted_iter(self):
        """Sorted iterator of the priority dictionary items.

        Beware: this will destroy elements as they are returned.
        """
        
        while self:
            yield self.pop_smallest()
## end of http://code.activestate.com/recipes/522995/ }}}

""" Here is my code, modified with heaps using priority_dict class"""

def dijkstra(G,v):
    #dist_so_far = [[0, v]]
    dist_so_far = priority_dict()
    dist_so_far[v] = 0
    final_dist = {}
    dist = {}
    dist[v] = 0
    while len(final_dist) < len(G) and len(dist_so_far) != 0:
        w = dist_so_far.pop_smallest()
        # lock it down!
        final_dist[w] = dist[w]
        
        for x in G[w]:
            if x not in final_dist:
                if x not in dist:
                    dist[x] = final_dist[w] + G[w][x]
                    dist_so_far[x] = final_dist[w] + G[w][x]
                elif final_dist[w] + G[w][x] < dist[x]:
                    dist[x] = final_dist[w] + G[w][x]
                    dist_so_far[x] = final_dist[w] + G[w][x]
    return final_dist

############
# 
# Test

def make_link(G, node1, node2, w):
    if node1 not in G:
        G[node1] = {}
    if node2 not in G[node1]:
        (G[node1])[node2] = 0
    (G[node1])[node2] += w
    if node2 not in G:
        G[node2] = {}
    if node1 not in G[node2]:
        (G[node2])[node1] = 0
    (G[node2])[node1] += w
    return G

""" test case given in Udacity website"""
def test():
    # shortcuts
    time1 = time.time()
    (a,b,c,d,e,f,g) = ('A', 'B', 'C', 'D', 'E', 'F', 'G')
    triples = ((a,c,3),(c,b,10),(a,b,15),(d,b,9),(a,d,4),(d,f,7),(d,e,3), 
               (e,g,1),(e,f,5),(f,g,2),(b,f,1))
    G = {}
    for (i,j,k) in triples:
        make_link(G, i, j, k)
    dist = dijkstra(G, a)
    assert dist[g] == 8 #(a -> d -> e -> g)
    assert dist[b] == 11 #(a -> d -> e -> g -> f -> b)
    time2 = time.time()
    print 'time taken: ', time2-time1

print test()

"""Original code by Prof MLL"""

def shortest_dist_node(dist):
    best_node = 'undefined'
    best_value = 1000000
    for v in dist:
        if dist[v] < best_value:
            (best_node, best_value) = (v, dist[v])
    return best_node

def dijkstra1(G,v):
    dist_so_far = {}
    dist_so_far[v] = 0
    final_dist = {}
    while len(final_dist) < len(G):
        w = shortest_dist_node(dist_so_far)
        #print 'w',w
        # lock it down!
        final_dist[w] = dist_so_far[w]
        del dist_so_far[w]
        for x in G[w]:
            if x not in final_dist:
                if x not in dist_so_far:
                    dist_so_far[x] = final_dist[w] + G[w][x]
                elif final_dist[w] + G[w][x] < dist_so_far[x]:
                    dist_so_far[x] = final_dist[w] + G[w][x]
    return final_dist
###

""" The tester below tests by comparing results from my modified code and
the original code by Prof MLL

Number of nodes in the random graph can be specified by manipulating variable, N"""

def test3(N):
    nodes=list(range(1,N))
    edges=[]
    for i in range(5*N):
      u=randint(1,N)
      v=randint(1,N)
      if u!=v:
        edges.append((u,v,randint(1,10)))
    G = {}
    for (i,j,k) in edges:
        make_link(G, i, j, k)
    dist = dijkstra1(G,1)
    dist2 = dijkstra(G,1)
    print 'dist', dist
    print 'dist2', dist2
    print dist == dist2
    counter = 1
    for key in dist:
           if dist2[key] != dist[key]:
               print 'dist2', key,':',dist2[key],'dist1',key,':',dist1[key]
               counter += 1
    print 'times wrong', counter

print test3(1200)

     

