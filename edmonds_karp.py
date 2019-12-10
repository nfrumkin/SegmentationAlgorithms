import numpy as np
import collections

# reference algorithm:
# https://en.wikipedia.org/wiki/Ford%E2%80%93Fulkerson_algorithm
class edmonds_karp():
    def __init__(self, graph):
        #input graph: adjacency matrix
        self.graph = graph
        self.num_nodes = graph.shape[0]
    
    def bfs(self, src, sink, parent):
        visited = np.zeros([self.num_nodes, 1])
        queue = collections.deque()
        queue.append(src)
        visited[src] = 1

        while queue:
            nd1 = queue.popleft()

            for nd2, flow in enumerate(self.graph[nd1,:]):
                if visited[nd2] == False and (flow > 0):
                    queue.append(nd2)
                    visited[nd2] = True
                    parent[nd2] = nd1
        
        # at end of BFS, return True if sink was visited
        return visited[sink]
    
    def edmonds_karp(self, src, sink):
        parent = -1*np.ones([self.num_nodes, 1], dtype=int)
        print(self.graph)
        max_flow = 0
        step = 0
        while self.bfs(src, sink, parent):
            print(step)
            step = step + 1
            path_flow = float("Inf")
            s = sink
            while s != src:
                path_flow = int(np.minimum(path_flow, self.graph[parent[s],s]))
                s = parent[s]
            max_flow += path_flow

            v = sink
            while v != src:
                u = parent[v]
                self.graph[u,v] = self.graph[u,v] - path_flow
                self.graph[v,u] = self.graph[v,u] + path_flow
                v = parent[u]
        print(self.graph)
        return max_flow

if __name__ == "__main__":
    a = np.zeros([12,12])
    a[1,2] = 1
    a[1,3] = 6
    a[1,4] = 4
    a[2,5] = 8
    a[3,6] = 2
    a[3,4] = 3
    a[3,2] = 1
    a[4,7] = 6
    a[5,6] = 3
    a[5,8] = 2
    a[6,9] = 4
    a[7,6] = 4
    a[7,10] = 100
    a[8,9] = 3
    a[8,11] = 8
    a[9,10] = 5
    a[9,11] = 6
    a[10,11] = 9

    # remove first row and column so indexing remains correct
    a = np.delete(a, (0), axis=0)
    a = np.delete(a, (0), axis=1)
    print("num_edges: ", np.count_nonzero(a))

    ek = edmonds_karp(a)
    
    max_flow = ek.edmonds_karp(0,10)
    print("max flow: ", max_flow)


