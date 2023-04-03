import csv
import queue
edgeFile = 'edges.csv'

def ucs(start, end):
    # Begin your code (Part 3)
    """
    1. Create a dictionary 'adj' to store the adjacency list of the map. 
        key: local start node     
        value: [local end node, distance from local start node to local end node]
    2. Use 'DictReader()' to read the csv file in the form of Python dictionary.
    3. Use 'dis' to store the distance from the global start node to the global end node.
        'vis' to store nodes which are visited by the ucs algorithm;
        'parent' to store the previous node in the path of each node;
        'pq' to store nodes which we are going to visit.
    4. Run a while loop until pq is empty or we have reached the global end node.
    5. In the while loop, we only visited each node at most once.
        We visited each neighbor of the current node, 
        recorded neighbors' parent, and push them and the distance from start node to them
        into the priority queue, which is a min heap data structure.
    6. Finally, we can find the distance and the reverse path from the global start node to 
        the global end node by the parent of each node. Since we only need the length of the
        path, there is no need to reverse the path at the end.
    """
    adj = dict()
    with open(edgeFile, 'r') as file:
        rows = csv.DictReader(file)
        for row in rows:
            key = int(row['start'])
            if key not in adj.keys():
                adj[key] = []
            adj[key].append([int(row['end']), float(row['distance'])])
            
    dis, vis, parent, pq = -1, list(), dict(), queue.PriorityQueue()
    pq.put([0, start])
    while pq:
        [d, u] = pq.get()
        if u == end:
            dis = d
            break
        if u in adj and u not in vis:
            vis.append(u)
            for v in adj[u]:
                if v[0] not in vis:
                    parent[v[0]] = u
                    pq.put([v[1] + d, v[0]])
    path = [end]
    cur = end
    while cur != start:
        cur = parent[cur]
        path.append(cur)
    return path, dis, len(vis)
    # End your code (Part 3)

if __name__ == '__main__':
    path, dist, num_visited = ucs(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
