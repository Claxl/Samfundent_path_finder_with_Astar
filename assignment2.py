from Map import Map_Obj


class Node():
    ## A node class for A* Pathfinding

    def __init__(self, pos, parent=None, weight=0, heuristic=0, total_cost=0):
        self.parent = parent
        self.pos = pos
        self.weight = weight
        self.heuristic = heuristic
        self.total_cost = total_cost

    ## Function to get an array of all child nodes
    def get_children(self, map):
        ## all possible neighbors of the current node
        child_positions = [[self.pos[0] - 1, self.pos[1]], [self.pos[0] + 1, self.pos[1]],
                           [self.pos[0], self.pos[1] - 1], [self.pos[0], self.pos[1] + 1]]
        child_nodes = []
        for child in child_positions:  # neighbors
            try:
                x = map.get_cell_value(child)
                ## Check if the cell is a wall
                if x >= 0:
                    weight = self.weight + x
                    heuristic = heuristic_comparison(child, map_obj.get_end_goal_pos())
                    total_cost = heuristic + weight
                    child_nodes.append(Node(child, self, weight, heuristic, total_cost))
            except IndexError:
                continue

        return child_nodes

    def compare_positions(self, other):
        if self.pos[0] == other[0] and self.pos[1] == other[1]:
            return True
        return False

## This function is used to find the shortest path between two nodes and is using the manhattan distance algorithm
def heuristic_comparison(first, other):
    (x1, y1) = first
    (x2, y2) = other
    return abs(x1 - x2) + abs(y1 - y2)

## This function is used to check if a node is already in the frontier or is already in the explored list
def already_in(node, list1, list2):
    for x, y in zip(list1, list2):
        if x.pos == node.pos:
            return x
        if y.pos == node.pos:
            return y
    return node


def star_search(map_obj):
    ## Create the first node from the start position
    node = Node(map_obj.get_start_pos())
    ## Create the frontier and the explored list to keep track of the nodes in the frontier and the explored list
    frontier, explored = [node], []

    while frontier:

        ## Remove first node from the frontier
        current_Node = frontier.pop()

        ## Add the current node to the explored list
        explored.append(current_Node)

        ## Check if the current node is the goal
        if current_Node.compare_positions(map_obj.get_goal_pos()):
            return current_Node

        ## Get neighbors of the current node
        child_nodes = current_Node.get_children(map_obj)

        for child in child_nodes:
            ## Check if the child node is already in the frontier or in the explored list
            new_child = already_in(child, frontier, explored)
            if new_child not in frontier and new_child not in explored:
                frontier.append(new_child)

        ## Sort the frontier by total cost descending order
        frontier.sort(key=lambda x: x.total_cost, reverse=True)
    return None


## This function is used to draw the path from the start to the goal on the map
def drawPathOnMap(node, map_obj, i=0):
    if i != 0:
        print("This is the task number ",i)
    x = node
    ## The loop goes through all the nodes in the path by traversing the path via each parent node
    while x.parent is not None:
        map_obj.set_cell_value(x.pos, 5)
        x = x.parent
    map_obj.show_map()


## This loop gives the result of the A* algorithm of all the tasks
for i in range(1,5):
    map_obj = Map_Obj(task=i)

    goalNode = star_search(map_obj)

    drawPathOnMap(goalNode, map_obj, i)
