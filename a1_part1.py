from typing import List, Dict, Tuple, Optional, Callable


# TODO: Complete the vertex class
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
        # TODO: Implement get_children
        # result = []
        # for key in self.children: # self.children is a dictionary
        #     child_tuple = self.children[key] # each edge is represented by a tuple
        #     result.append(child_tuple)
        # return result
        # similarly this can be done in 1 line of code
        return list(self.children.values())


# TODO: Complete the graph class
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
        # TODO: implement is_child
        # self.vertices is a list of Vertex objects
        # each Vertex object has a name (str) and children
        for v in self.vertices:
            if v.name == v_name: # find out if such vertex even exists
                # v.children is a dictionary of v's children
                for edge in v.get_children():
                    # each child edge is represented by a (parent name, child name, weight) tuple
                    if edge[1] == u_name:
                        return True
                # for v_child in v.children:
                #     if v.children[v_child][1] == u_name:
                #         return True
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
        # if self.is_child(v_name, u_name) is True:
        #     return
        if self.is_child(u_name, v_name) is True:
            # find the vertex u
            parent_vertex = next(
                (vertex for vertex in self.get_vertices() if vertex.name == u_name),
                None
            )
            for edge in parent_vertex.get_children():
                if edge[1] == v_name:
                    return edge
        return None
        # find out if there is a parent-child relationship
        # if u is a child of v
       #  if self.is_child(v_name, u_name) is True:
       #      return None
       # if self.is_child(u_name, v_name) == True:
       #      return None
       #  # otherwise return false
       # return None

