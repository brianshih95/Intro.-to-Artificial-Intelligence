import csv
import queue
edgeFile = 'edges.csv'

def dfs(start, end):
    # Begin your code (Part 2)
    """
    1. Create a dictionary 'adj' to store the adjacency list of the map. 
        key: local start node     
        value: [local end node, distance from local start node to local end node]
    2. Use 'DictReader()' to read the csv file in the form of Python dictionary.
    3. Use 'vis' to store nodes which are visited by the dfs algorithm;
        'parent' to store the previous node in the path of each node;
        'dis' to store the distance from the previous node to the current node of each node;
        's' to store nodes which we are going to visit.
    4. Run a while loop until s is empty or we have reached the global end node.
    5. In the while loop, we only visited each node at most once.
        We visited each neighbor of the current node, 
        and recorded neighbors' parent, distance, and then push them into the stack,
        which is an LIFO data structure.
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
    
    vis, parent, dis, s = [], dict(), dict(), queue.LifoQueue()
    s.put(start)
    while s:
        u = s.get()
        if u == end:
            break
        if u in adj:
            for v in adj[u]:
                if v[0] not in vis:
                    vis.append(v[0])
                    parent[v[0]] = u
                    dis[v[0]] = v[1]
                    s.put(v[0])
    path = [end]
    total_dis = 0
    cur = end
    while cur != start:
        total_dis += dis[cur]
        cur = parent[cur]
        path.append(cur)
    return path, total_dis, len(vis)
    # End your code (Part 2)

if __name__ == '__main__':
    path, dist, num_visited = dfs(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
