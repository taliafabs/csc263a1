from typing import List, Dict, Tuple, Optional, Callable


class Vertex:
    """
    Represents a vertex in a graph.

    Attributes:
        name (str): The label or identifier of the vertex.
        children (Dict[str, Tuple[str, str, float]]): 
            A mapping between child vertex names and edges.
            Each edge is represented as a tuple:
                (source vertex name, child vertex name, edge weight).
    """

    def __init__(self, name: str, children: Optional[Dict[str, Tuple[str, str, float]]] = None):
        """
        Initializes a Vertex.

        Args:
            name (str): The label or identifier of the vertex.
            children (Optional[Dict[str, Tuple[str, str, float]]]): 
                A mapping between child vertex names and edges.
        """
        self.name = name
        self.children: Dict[str, Tuple[str, str, float]] = children if children is not None else {}

    def get_children(self) -> List[Tuple[str, str, float]]:
        """
        Returns all edges from this vertex.

        Returns:
            List[Tuple[str, str, float]]: The list of edges from this vertex.
        """
        return list(self.children.values())


class Graph:
    """
    Represents a graph consisting of multiple vertices.

    Attributes:
        vertices (List[Vertex]): The list of vertices in the graph.
    """

    def __init__(self, vertices: List[Vertex]):
        """
        Initializes a Graph.
    
        Args:
            vertices (List[Vertex]): The list of vertices that make up the graph.
        """
        self.vertices = vertices

    def get_vertices(self) -> List[Vertex]:
        """
        Returns all vertices in the graph.

        Returns:
            List[Vertex]: The list of vertices in the graph.
        """
        # TODO: implement get_vertices
        return self.vertices

    def is_child(self, u_name: str, v_name: str) -> bool:
        """
        Checks if vertex v_name is a child of vertex u_name.

        Args:
            u_name (str): The name of the parent vertex.
            v_name (str): The name of the potential child vertex.

        Returns:
            bool: True if the vertex v_name is a child of the vertex u_name, False otherwise.
        """
        # TODO: Implement is_child
        for v in self.get_vertices():
            if v.name == u_name:  # find parent vertex (vertex with u_name)
                for e in v.get_children():  # go thru its (parent, child, weight) edges
                    if e[1] == v_name:
                        return True  # return true if child's name matches
        return False

    def get_edge(self, u_name: str, v_name: str) -> Optional[Tuple[str, str, float]]:
        """
        Retrieves the edge between u_name and v_name.

        Args:
            u_name (str): The name of the parent vertex.
            v_name (str): The name of the child vertex.

        Returns:
            Optional[Tuple[str, str, float]]: The edge if it exists, 
            or None if no such edge is found.
        """
        # TODO: implement get_edge
        if self.is_child(u_name, v_name) is True:
            parent = None
            for v in self.get_vertices():
                if v.name == u_name:
                    parent = v
            for edge in parent.get_children():
                if edge[1] == v_name:
                    return edge
        return None

    # My new helper functions
    def find_vertex(self, n: str) -> Optional[Vertex]:
        for vertex in self.get_vertices():
            if vertex.name == n:
                return vertex
        return None
    def add_vertex(self, name: str):
        """
        Helper function to add a vertex to a graph

        Args:
            name (str): The name of the new vertex

        Returns:

        """
        # TODO: Implement add_vertex
        # check if a vertex with that name exists??
        # add the new vertex
        vertex = Vertex(name)
        self.vertices.append(vertex)

    def add_edge(self, origin_name: str, destination_name: str, weight: float):
        """
        Helper function to add an edge to a graph

        Args:
            origin_name (str): the name of the origin (parent) vertex
            destination_name (str): the name of the destination (child) vertex
            weight (float): the weight of the edge

        Returns:
        """
        # TODO: implement add_edge
        # don't do anything if edge exists
        if self.get_edge(origin_name, destination_name) is not None:
            return

        origin_vertex = self.find_vertex(origin_name)
        destination_vertex = self.find_vertex(destination_name)
        if origin_vertex is None:
            # origin_vertex = Vertex(origin_name)
            self.add_vertex(origin_name)
        if destination_vertex is None:
            # destination_vertex = Vertex(destination_name)
            self.add_vertex(destination_name)
        origin_vertex.children[destination_name] = (origin_name, destination_name, weight)


class Device(Vertex):
    """
    Represents a network device, extending the Vertex class with
    device-specific functionality.

    Attributes:
        name (str): The label or identifier of the device.
        children (Dict[str, Tuple[str, str, float]]): 
            A mapping between child device names and nearby devices.
        network (Graph): A graph representing this device's discovered network.
    """

    def __init__(self, name: str, children: Optional[Dict[str, Tuple[str, str, float]]] = None,
                 network: Optional[Graph] = None):
        """
        Initializes a Device.

        Args:
            name (str): The label or identifier of the device.
            children
            network
        """
        # TODO: initialize the device class
        super().__init__(name, children={})
        self.network = Graph([self])  # should represent the device's discovered network
        # initially, the devices discovered network only includes itself

    def discover_network(self, find_devices_fn: Callable[[List[str]], List[Tuple[str, str, float]]]) -> None:
        """
        Discovers the surrounding network starting from this device. Once this 
        function is called, self.network should contain a representation of the 
        device's discovered network.

        Args:
            find_devices_fn (Callable[[List[str]], List[Tuple[str, str, float]]]): 
                A function that takes an ordered list of device names (i.e., a path) 
                and returns the edges from the last device in the path to its immediate children.
        """
        # TODO: Implement discover_network
        visited = set()
        queue = [[self.name]] # FIFO

        while queue:
            path = queue.pop(0)
            curr = path[-1]

            if curr in visited:
                continue
            visited.add(curr)

            edges = find_devices_fn(path)

            for edge in edges:
                self.network.add_edge(edge[0], edge[1], edge[2])
                if edge[1] not in visited:
                    queue.append(path + [edge[1]])
            # curr_vertex = self.network.find_vertex(curr)
            # for edge in edges:
            #     if curr_vertex.name == edge[0]:
            #         curr_vertex.children[edge[1]] = edge


        # visited = set()
        # queue = [[self.name]]
        # while queue:
        #     pass
        # visited = set()  # empty set to keep track of visited devices
        # queue = [[self.name]]  # queue with only the initial device
        # while queue:
        #     path = queue.pop(0)  # remove the first device from the queue
        #     curr = path[-1]
        #     if curr in visited:
        #         continue
        #     visited.add(curr)
        #     edges = find_devices_fn(path)
        #     for (origin, destination, weight) in edges:
        #         if not (destination in self.network.get_vertices()):
        #             new_device_vertex = Device(destination)
        #             self.network.vertices.append(new_device_vertex)  # add a new vertex, might define func for it
        #         # add the edge


    def find_path(self, d_name: str) -> Optional[List[str]]:
        """
        Finds the cheapest path from this device to the specified target device 
        using the Cheapest-First Search (CFS) algorithm.

        Args:
            d_name (str): The name of the destination device.

        Returns:
            Optional[List[str]]: An ordered list of device names representing the path 
            from this device to the target. If no path exists, returns None.
        """
        # TODO: implement find_path
        # find out if it is even possible to find a path
        d_vertex = None
        for vertex in self.network.get_vertices():
            if vertex.name == d_name:
                d_vertex = vertex
        # if no vertex with d_name exists in self.network connected graph, return None
        if d_vertex is None:
            return None

        # now that we have established that a path exists, find the cheapest path
        dummy_node = ([self.name], 0.0)
        open = [dummy_node]
        closed = [dummy_node]
        closed_destinations = [self.name] # might need to use this for inter-path cycle checking
        while open:
            pass



        # start by checking if such a path even exists
            # check if a vertex with d_name exists in self.network

        # once we know that the vertex is in-network ...

        # v0 = self.name
        # dummy_path = ([v0], 0.0)
        # open = set(dummy_path) # find a way to order by weight
        # closed = set(dummy_path)
        # closed_destinations = [v0]
        #
        # # if no path



        # v0 = self.name # the starting vertex name
        # open = [([v0], 0.0)] # set of open nodes initially only contains dummy path
        # closed = [open[0]] # empty set of closed nodes. mark a node visited as soon as it is added to O
        #
        # # find the cheapest "path" node in the set of open nodes
        # while open:
        #     pass
        #
        # curr_cheap = None
        #
        # # perform cycle check
        # for path_node in closed:
        #     pass
        #
        # # export to set of open noes
        # open.append(curr_cheap)
        # closed.append(curr_cheap)
        #
        # # explore node










# ----------------------------------------------------------------------
# Mock function for testing
# ----------------------------------------------------------------------
def find_devices_fn(path: List[str]) -> List[Tuple[str, str, float]]:
    """
    A mock function that simulates network discovery.

    Args:
        path (List[str]): The sequence of device names representing the discovery path.

    Returns:
        List[Tuple[str, str, float]]: A list of edges, where each tuple contains:
            - source device name (str),
            - child device name (str),
            - edge weight (float).
    """
    # base: the empty path
    if not path:
        return []

    # otherwise, for the non-empty path
    last_device = path[-1]  # get the device at the very end of the path

    # this is the mock network being used
    # mock_network is a dictionary
    # each key in the mock_network dictionary is the name of a vertex
    # each index is a list of tuples w/ the len 1 path to each of its children and the weight
    mock_network = {
        "chandra-s25": [
            ("chandra-s25", "router-051797", 1.0),
            ("chandra-s25", "helen-pc", 2.0),
        ],
        "router-051797": [
            ("router-051797", "ws-102", 1.2),
            ("router-051797", "switch-12", 0.8),
            ("router-051797", "srv-07", 1.0),
        ],
        "helen-pc": [
            ("helen-pc", "ws-14", 1.5),
        ],
    }

    return mock_network.get(last_device, [])
