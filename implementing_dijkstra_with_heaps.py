""" Utility Functions"""

import time
from random import randint
import heapq
from priority_dictionary import priority_dict

""" priority_dict class was used to  implement heaps efficiently. The class makes it
possible to update the dictionary key values in constant time. The class was taken from
the url given below."""


""" Here is my code, modified with heaps using priority_dict class"""

def dijkstra(G,v):
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
    counter = 0
    for key in dist:
           if dist2[key] != dist[key]:
               print 'dist2', key,':',dist2[key],'dist1',key,':',dist1[key]
               counter += 1
    print 'times wrong', counter
    print len(dist)
print test3(1200)
     

