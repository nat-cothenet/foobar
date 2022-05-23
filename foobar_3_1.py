class Path:
    def __init__(self, node_list, elim_remaining):
        # List of Node objects
        self.node_list = node_list

        # Number of potential wall eliminations remaining
        self.elim_remaining = elim_remaining

    def __repr__(self):
        return "(" + str(self.node_list) + ", elim_rem=" + str(self.elim_remaining) + ")"


class Node:
    def __init__(self, x, y, wall, num_elims=0):
        # Coordinates (int)
        self.x = x
        self.y = y

        # Boolean indicating whether map at this index is a wall
        self.wall = wall

        # Booleans indicating whether these coordinates have yet been visited
        # and the number of wall eliminations that have occurred prior to being visited

        # This is because we want to track visited nodes to decrease runtime
        # (if a node has already been visited on a shorter route, continuing on
        # that path would be redundant); however, the same node visited on a path
        # where a different number of walls can still be eliminated in the future
        # does not create a redundant problem (they have different potential solution
        # sets stemming from that single node)

        # For flexibility, we represent the visitation status as a vector (list) where
        # the index of the list represents the number of eliminations *remaining* when
        # this node is visited. So self.visited[0] indicates whether the Node has been
        # visited with no remaining wall eliminations (i.e., already having eliminated
        # all potential walls)
        self.visited = [False] * (num_elims + 1)


def solution(station_map):
    """
    Given a station map (list of list of binary integers) indicating where walls (1)
    or open corridors (0) are present, returns the shortest path from the upper right-hand
    corner of the map (index [0, 0]) to the lower left-hand corner (index [m, n] for a map
    of width m and height n). The map dimensions must be between 2 and 20 units. Starting and
    ending nodes are included in the path length.

    If inputs are invalid, returns -1. If no valid path can be found, returns -99.
    :param station_map: list of list of binary integers indicating walls (1) or open space (0)
    on a 2D grid
    :return: length of shortest path from LHS upper corner to RHS lower corner; \
    -1 if invalid inputs, -99 if no solution
    """
    # num_elims is the number of walls that can be removed
    num_elims = 1

    # Check that our map size is compliant

    # Map height
    y_max = len(station_map)

    if y_max < 2 or y_max > 20:
        return -1

    # Map width
    x_max = len(station_map[0])

    if x_max < 2 or x_max > 20:
        return -1

    # Create a map of Nodes
    station_map_nodes = [
        [Node(i, j, station_map[j][i] == 1, num_elims) for i in range(x_max)]
        for j in range(y_max)
    ]

    # Specify the starting node and set as having been visited
    start = station_map_nodes[0][0]
    start.visited[num_elims] = True
    start_path = Path(
        node_list=[start],
        elim_remaining=num_elims,
    )

    # Specifies the *index* of the final node (success criterion)
    end_index = [x_max - 1, y_max - 1]

    # Finds the shortest path starting with the starting node [0, 0] and ending at the end_index
    shortest_path = path_start_to_end([start_path], end_index, station_map_nodes)

    if not shortest_path:
        return -99

    # Returns the length of the shortest path
    return len(shortest_path.node_list)


def get_neighbors(node, x_max, y_max):
    """ Returns the indices of all valid neighbors to the current node
    :param node: Node for which we want to extract a list of neighbors
    :param x_max: width of the map that will limit the index of valid neighbors
    :param y_max: height of the map that will limit the index of valid neighbors
    :return: list of 2-element lists [x, y] containing the coordinates of \
    neighbors that are within the bounds of the map
    """
    neighbors = []
    x = node.x
    y = node.y

    if x >= x_max or y >= y_max or x < 0 or y < 0:
        return []

    if x > 0:
        neighbors.append([x - 1, y])
    if x < x_max - 1:
        neighbors.append([x + 1, y])
    if y > 0:
        neighbors.append([x, y - 1])
    if y < y_max - 1:
        neighbors.append([x, y + 1])

    return neighbors


def path_start_to_end(paths, end, station_map):
    """
    Given a set of "root" paths (list of Paths of Nodes), extends the paths to valid neighbors of \
    their ending Node until the end index is reached
    :param paths: list of Paths (containing a list of Nodes) that are the "roots" (beginning \
    portions) of all potentially successful Paths to arrive at the end index
    :param end: index (2-element list [x, y]) indicating the position in the station_map of the \
    end node
    :param station_map: list of list of Nodes indicating presence of walls, visited status, and \
    coordinates
    :return: Path describing the shortest number of Nodes we must visit to link our starting \
    path(s) to the end index
    """
    if paths is None or len(paths) == 0:
        return None

    new_paths = []
    # Iterates over all "root" paths to look for potential extensions of the
    # ending Node. All paths that are extended are then passed to the function
    # recursively
    for path in paths:
        # Check that path exists and contains at least one Node
        if path is None or path.node_list is None or len(path.node_list) == 0:
            continue

        # Sets the current node to the last node in the path
        node = path.node_list[-1]

        # Checks for success criterion
        if [node.x, node.y] == end:
            return path

        # Gets valid neighboring coordinates
        neighbors = get_neighbors(node=node, x_max=len(station_map[0]), y_max=len(station_map))
        if len(neighbors) == 0:
            continue

        # For each neighbor, checks whether this is a valid addition to the current path
        # (has not yet been visited with the current number of wall eliminations; if it
        # is a wall, make sure we can eliminate it before adding), creates a copy of the
        # path and adds the neighbor node, and adds the new path to the list of Paths that
        # become our new potential path "roots"
        for node_index in neighbors:
            next_node = station_map[node_index[1]][node_index[0]]
            # Check if this next node has already been visited with this elimination status
            # If so, don't continue with this next node (will be redundant)
            if next_node.visited[path.elim_remaining]:
                continue

            # Flag the node as having been visited (on a path that
            # has or has not included an elimination)
            next_node.visited[path.elim_remaining] = True

            # Add node to path
            new_path = Path(
                [p for p in path.node_list] + [next_node],
                path.elim_remaining
            )

            # If the final node has been added, return this path
            if [next_node.x, next_node.y] == end:
                return new_path

            # If the node has not been visited and is not the end state,
            # then we may be able to add it to the list of potential paths

            # If the node is not a wall, add it to the list of potential paths
            if not next_node.wall:
                new_paths.append(new_path)
            # If the node is a wall but we can eliminate one of our walls, add it to
            # the list of potential paths and decrement the # of walls we can eliminate
            elif next_node.wall and new_path.elim_remaining > 0:
                new_path.elim_remaining -= 1
                new_paths.append(new_path)
    return path_start_to_end(new_paths, end, station_map)

"""
class Node:
    def __init__(self, x, y, x_max, y_max, visited=False, wall=False, elim=1):
        self.x = x
        self.y = y
        self.visited = visited
        self.wall = wall
        self.distance = float("inf")
        self.elim = elim
        self.neighbors = self.set_neighbors(x_max, y_max)

    def set_neighbors(self, x_max, y_max):
        neighbors = []
        if self.x > 0:
            neighbors.append([self.x - 1, self.y])
        if self.x < x_max - 1:
            neighbors.append([self.x + 1, self.y])
        if self.y > 0:
            neighbors.append([self.x, self.y - 1])
        if self.y < y_max - 1:
            neighbors.append([self.x, self.y + 1])
        return neighbors

    def __repr__(self):
        return ("[x=" + str(self.x) + ", y=" + str(self.y) + "; d=" + str(self.distance) + \
                ", v=" + str(self.visited) + ", w=" + str(self.wall) + ", n="+str(self.neighbors)+"]\n")

def solution3(map):
    # r is the number of walls that can be removed
    r = 1

    # map height
    y_max = len(map)

    if y_max == 0:
        return -1

    # map width
    x_max = len(map[0])

    if x_max == 0:
        return -1

    # Define end node
    end_node = Node(
        x=x_max - 1, y=y_max - 1,
        x_max=x_max, y_max=y_max,
        visited=False,
        wall=(map[y_max - 1][x_max - 1] == 1),
        elim=r
    )

    # Define starting node and initialize
    start_node = Node(
        x=0, y=0,
        x_max=x_max, y_max=y_max,
        visited=True,
        wall=(map[y_max - 1][x_max - 1] == 1),
        elim=r
    )
    start_node.distance = 1

    # Initialize queue as starting node
    queue = [start_node]

    # Iteratively solve for minimum path
    p = path_from_node_iter2(queue, end_node, map)

    return p

def path_from_node_iter2(queue, end_node, map):
    while len(queue) > 0:
        curr_node = queue.pop(0)
        curr_node.visited = True

        if curr_node.x == end_node.x and curr_node.y == end_node.y:
            return curr_node.distance

        for node_index in curr_node.neighbors:
            node = Node(
                x=node_index[0], y=node_index[1],
                x_max=len(map[0]), y_max=len(map),
                visited=True,
                wall=(map[node_index[1]][node_index[0]] == 1),
                elim=curr_node.elim
            )
            node.distance = curr_node.distance + 1

            if node.x == end_node.x and node.y == end_node.y:
                return node.distance
            if not node.wall or (node.wall and node.elim > 0):
                if node.wall:
                    node.elim -= 1
                queue.append(node)

    return None


def solution2(map):
    # r is the number of walls that can be removed
    r = 1

    # map height
    y_max = len(map)

    if y_max == 0:
        return -1

    # map width
    x_max = len(map[0])

    if x_max == 0:
        return -1

    node_map = [
        [
            Node(
                x=i,
                y=j,
                x_max=x_max,
                y_max=y_max,
                visited=False,
                wall=map[j][i] == 1,
                elim=r
            ) for i in range(x_max)
        ]
        for j in range(y_max)
    ]

    # Define end node
    end_index = [x_max - 1, y_max - 1]
    end = node_map[end_index[1]][end_index[0]]

    # Define starting node and initialize
    start_index = [0, 0]
    node_map[start_index[1]][start_index[0]].visited = True
    node_map[start_index[1]][start_index[0]].distance = 1

    # Initialize queue as starting node
    queue = [node_map[start_index[1]][start_index[0]]]

    # Iteratively solve for minimum path
    p = path_from_node_iter(queue, end, node_map)

    return p



def path_from_node_iter(queue, end, map):
    while len(queue) > 0:
        curr_node = queue.pop(0)
        map[curr_node.y][curr_node.x].visited = True

        if curr_node.x == end.x and curr_node.y == end.y:
            return curr_node.distance

        for node_index in curr_node.neighbors:
            node = map[node_index[1]][node_index[0]]
            if node.x == end.x and node.y == end.y:
                return curr_node.distance + 1
            if not node.visited:
                if not node.wall or (node.wall and curr_node.elim > 0):
                    node.distance = curr_node.distance + 1
                    if node.wall:
                        node.elim -= 1
                    else:
                        node.elim = curr_node.elim
                    queue.append(node)

    return None



def path_from_node(queue, end, map):
    if not queue:
        print("abort!")
        return

    curr_node = queue.pop(0)

    print("Curr node:\t" + str(curr_node))
    if curr_node.x == end.x and curr_node.y == end.y:
        print("won 2!")
        print(curr_node.distance)
        return curr_node.distance

    for node_index in curr_node.neighbors:
        node = map[node_index[1]][node_index[0]]
        print(node)
        if node.x == end.x and node.y == end.y:
            print("won!")
            print(curr_node.distance)
            return curr_node.distance + 1
        if not node.visited:
            if not node.wall or (node.wall and curr_node.elim > 0):
                map[node_index[1]][node_index[0]].visited = True
                map[node_index[1]][node_index[0]].distance = curr_node.distance + 1
                if node.wall:
                    map[node_index[1]][node_index[0]].elim -= 1
                else:
                    map[node_index[1]][node_index[0]].elim  = curr_node.elim
                queue.append(map[node_index[1]][node_index[0]])
    print("Queue:\t" + str(queue))
    path_from_node(queue, end, map)
"""


if __name__ == '__main__':
    print(solution([[0, 0], [0, 0]]))
    print(solution([[0, 1], [1, 0]]))
    print(solution([[0, 0, 1, 0], [0, 0, 1, 1], [0, 0, 1, 0], [0, 0, 1, 0]]))
    print(solution([[0, 1, 1, 0], [0, 0, 0, 1], [1, 1, 0, 0], [1, 1, 1, 0]]))
    print(solution([[0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 0], [0, 0, 0, 0, 0, 0], [0, 1, 1, 1, 1, 1], [0, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0]]))
    print(solution([[0, 1, 1, 0, 0, 0], [1, 1, 1, 0, 1, 0], [0, 0, 1, 0, 1, 0], [1, 0, 1, 0, 1, 0], [1, 0, 0, 0, 1, 0]]))
    board = [[0 for i in range(20)] for j in range(20)]
    print(solution(board))