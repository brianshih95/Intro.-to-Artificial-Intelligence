import csv
import queue
edgeFile = 'edges.csv'
heuristicFile = 'heuristic.csv'

def astar_time(start, end):
    # Begin your code (Part 6)
    """
    1. Create a dictionary 'adj' to store the adjacency list of the map. 
        key: local start node     
        value: [local end node, distance from local start node to local end node]
    2. Create a dictionary 'straight_dis' to store the straight distance
        from the local end node to the global end node. 
        key: local start node    
        value: straight distance from the local end node to the global end node
    3. Use 'DictReader()' to read the csv file in the form of Python dictionary.
    4. Use 'time' to store the time from the global start node to the global end node.
        'vis' to store nodes which are visited by the A* algorithm;
        'parent' to store the previous node in the path of each node;
        'pq' to store nodes which we are going to visit.
    5. Run a while loop until pq is empty or we have reached the global  node.
    6. In the while loop, we only visited each node at most once.
        We visited each neighbor of the current node, 
        recorded neighbors' parent, and push them, the time to travel from 
        the global start node to them and the estimated cost into the priority queue,
        which is a min heap data structure.
    7. The heuristic function is the ratio of the straight distance to the maximum speed limit.
    8. Finally, we can find the distance and the reverse path from the global start node to 
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
            adj[key].append([int(row['end']), float(
                row['distance']), float(row['speed limit'])])
    
    heuristic = dict()
    with open(heuristicFile, 'r') as file:
        rows = csv.DictReader(file)
        for row in rows:
            heuristic[int(row['node'])] = float(row[str(end)])
    time, vis, parent, pq = 0, list(), dict(), queue.PriorityQueue()
    pq.put([0, 0, start])
    while pq:
        [f, t, u] = pq.get()
        if u == end:
            time = t
            break
        if u in adj and u not in vis:
            vis.append(u)
            for v in adj[u]:
                if v[0] not in vis:
                    parent[v[0]] = u
                    pq.put([heuristic[v[0]] / (100/3.6) + v[1] / (v[2]/3.6) + t,
                            v[1] / (v[2]/3.6) + t, v[0]])
    
    path = [end]
    cur = end
    while cur != start:
        cur = parent[cur]
        path.append(cur)
    return path, time, len(vis)
    # End your code (Part 6)

if __name__ == '__main__':
    path, time, num_visited = astar_time(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total second of path: {time}')
    print(f'The number of visited nodes: {num_visited}')
