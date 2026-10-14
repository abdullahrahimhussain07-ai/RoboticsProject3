import heapq

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star_search(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    open_list = []
    heapq.heappush(open_list, (0 + heuristic(start, goal), 0, start, [start]))
    closed_set = set()
    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    
    while open_list:
        f, g, current, path = heapq.heappop(open_list)
        if current == goal:
            return path
        if current in closed_set:
            continue
        closed_set.add(current)
        
        for dr, dc in neighbors:
            neighbor = (current[0] + dr, current[1] + dc)
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols:
                if grid[neighbor[0]][neighbor[1]] == 0 and neighbor not in closed_set:
                    tentative_g = g + 1
                    tentative_f = tentative_g + heuristic(neighbor, goal)
                    heapq.heappush(open_list, (tentative_f, tentative_g, neighbor, path + [neighbor]))
    return None
