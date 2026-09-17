from utils import move_to

def neighbors(current):
    ret = []
    for dir,dx,dy in [(North, 0, 1), (South, 0, -1), (East, 1, 0), (West, -1, 0)]:
        if can_move(dir):
            ret.append((current[0]+dx, current[1]+dy))
    return ret

def step_maze(current=(get_pos_x(), get_pos_y()), goal=measure(), visited=None, path=None):
    if visited == None:
        visited = set()
    if path == None:
        path = []
    visited.add(current)
    path.append(current)
    if current == goal:
        harvest()
        return True
    for neighbor in neighbors(current):
        if neighbor not in visited:
            move_to(neighbor[0], neighbor[1])
            if step_maze(neighbor, goal, visited, path):
                return True
    # Backtrack
    path.pop()
    if path:
        move_to(path[-1][0], path[-1][1])
    return False
