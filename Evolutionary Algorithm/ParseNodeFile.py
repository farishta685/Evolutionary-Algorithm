class Node:
    def __init__(self, location_num, x, y):
        self.location_num = location_num
        self.x = x
        self.y = y


def parse_node_file(file_location):
    parse_after_string = "NODE_COORD_SECTION\n"
    
    node_array = []
    parsing_nodes = False
    node_file = open(file_location, "r")

    for line in node_file:
    
        # Check For End Of File
        if line == "EOF\n":
            parsing_nodes = False
        
        # Creating The Nodes And Putting Them Into A Class
        if parsing_nodes is True:
            split_line = line.split()

            # If there are three elements, read the line
            if len(split_line) == 3:
                current_node = Node(int(split_line[0]), float(split_line[1]), float(split_line[2]))
                node_array.append(current_node)
            else:
                parsing_nodes = False

        # Check To See If Declared Node Section, To Begin Parsing
        if line == parse_after_string:
            parsing_nodes = True
    
    # Return Node Array From Function
    return node_array


def print_nodes(nodes):
    for selected_node in nodes:
        print("Node Num: ", selected_node.location_num, "\tNode x: ", selected_node.x, "\tNode y: ", selected_node.y)
