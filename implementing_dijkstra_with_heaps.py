#
# The code below uses a linear
# scan to find the unfinished node
# with the smallest distance from
# the source.
#
# Modify it to use a heap instead
# 
import time
from random import randint
import heapq

def shortest_dist_node(dist):
    best_node = 'undefined'
    best_value = 1000000
    for v in dist:
        if dist[v] < best_value:
            (best_node, best_value) = (v, dist[v])
    return best_node

def dijkstra(G,v):
    dist_so_far = [[0, v]]
    final_dist = {}
    dist = {}
    while len(final_dist) < len(G):
        print dist_so_far
        w = dist_so_far[0][1]
        print 'w', w
        # lock it down!
        final_dist[w] = dist_so_far[0][0]
        heapq.heappop(dist_so_far)
        
        for x in G[w]:
            if x not in final_dist:
                if x not in dist:
                    heapq.heappush(dist_so_far, [final_dist[w] + G[w][x], x])
                    dist[x] = final_dist[w] + G[w][x]
                elif final_dist[w] + G[w][x] < dist[x]:
                    heapq.heappush(dist_so_far, [final_dist[w] + G[w][x], x])
                    dist[x] = final_dist[w] + G[w][x]
        raw_input()
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


def test():
    # shortcuts
    time1 = time.time()
    (a,b,c,d,e,f,g) = ('A', 'B', 'C', 'D', 'E', 'F', 'G')
    triples = ((a,c,3),(c,b,10),(a,b,15),(d,b,9),(a,d,4),(d,f,7),(d,e,3), 
               (e,g,1),(e,f,5),(f,g,2),(b,f,1))
    G = {}
    for (i,j,k) in triples:
        make_link(G, i, j, k)

    dist = dijkstra1(G, a)
    assert dist[g] == 8 #(a -> d -> e -> g)
    assert dist[b] == 11 #(a -> d -> e -> g -> f -> b)
    time2 = time.time()
    print 'time taken: ', time2-time1
'''
print test()


def test2(N):
    # shortcuts
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
    dist = dijkstra(G,1)

#test()

for N in [100,300,600,1000,3000,6000,10000,30000,60000,100000]:
  time1 = time.time()
  print(N)
  test2(N)
  time2 = time.time()
  print 'time bro', time2-time1

print test()    


'''
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
        print 'w',w
        # lock it down!
        final_dist[w] = dist_so_far[w]
        del dist_so_far[w]
        for x in G[w]:
            if x not in final_dist:
                if x not in dist_so_far:
                    dist_so_far[x] = final_dist[w] + G[w][x]
                elif final_dist[w] + G[w][x] < dist_so_far[x]:
                    dist_so_far[x] = final_dist[w] + G[w][x]
        raw_input()
    return final_dist


'''
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
            counter += 1
    print 'times wrong', counter
    
print test3(1000)

'''           

print test()
