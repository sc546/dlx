import argparse

class HeaderNode:
    def __init__(self, item):
        self.item = item

class ItemNode:
    def __init__(self):
        pass

class Graph:
    def __init__(self, universe, sets):
        self.reset_graph()
        self.create_graph(universe, sets)

    def reset_graph(self):
        self.dummy_node = None

        self.left  = {}
        self.right = {}

        self.up   = {} # Top of the column
        self.down = {} # First in the row

        self.header   = {}
        self.leftmost = {}

        self.row_num = {}

    def create_graph(self, universe, sets):
        self.dummy_node = HeaderNode(None)
        header_nodes = [self.dummy_node] + [HeaderNode(item) for item in universe]
        
        self.left  = {node2: node1 for node1, node2 in zip(header_nodes[:-1], header_nodes[1:])}
        self.right = {node1: node2 for node1, node2 in zip(header_nodes[:-1], header_nodes[1:])}
        
        # Unlike in the original paper, links do not wrap around.
        # This way we have terminating nodes for both rows and colums,
        # and can stop iterating by checking for them.

        self.left[header_nodes[0]] = None
        self.right[header_nodes[-1]] = None

        for node in header_nodes:
            self.up[node] = None

        prev = {node.item: node for node in header_nodes[1:]}
        item_to_header = {node.item: node for node in header_nodes[1:]}

        for set_idx, s in enumerate(sets):
            item_nodes = []
            for item in s:
                if item not in universe:
                    print(f"ERROR: Item {item} in set {set_idx+1} is not in universe")
                    self.reset_graph()
                    return

                item_node = ItemNode()
                item_nodes.append(item_node)

                self.header[item_node] = item_to_header[item]

            for item_node in item_nodes:
                self.leftmost[item_node] = item_nodes[0]
                self.row_num[item_node] = set_idx+1
            
            for prev_i, node in enumerate(item_nodes[1:]):
                self.left[node] = item_nodes[prev_i]

            for i, node in enumerate(item_nodes[:-1]):
                self.right[node] = item_nodes[i+1]

            self.left[item_nodes[0]] = None
            self.right[item_nodes[-1]] = None

            for item, node in zip(s, item_nodes):
                self.up[node] = prev[item]
                self.down[node] = None

                self.down[self.up[node]] = node

                prev[item] = node

    def solve(self):
        if not self.dummy_node:
            return False, []

        history = []
        
        def cover(node):
            assert isinstance(node, ItemNode)
            nonlocal history

            def cover_node(node):
                if self.right[node]: self.left[self.right[node]] = self.left[node]
                if self.left[node]:  self.right[self.left[node]] = self.right[node]
                if self.down[node]:  self.up[self.down[node]] = self.up[node]
                if self.up[node]:    self.down[self.up[node]] = self.down[node]
            
            covered = []
            
            def cover_row(node):
                assert isinstance(node, ItemNode)
                nonlocal covered

                current = self.leftmost[node]
                while current:
                    cover_node(current)
                    covered.append(current)

                    current = self.right[current]

            def cover_column(header):
                assert isinstance(header, HeaderNode)
                nonlocal covered

                current = self.down[header]
                while current:
                   cover_row(current)
                   current = self.down[current]

                cover_node(header)
                covered.append(header)
       
            current = self.leftmost[node]
            while current:
                header = self.header[current]
                cover_column(header)

                current = self.right[current]

            history.append(covered)

        def uncover(node):
            assert isinstance(node, ItemNode)
            nonlocal history

            def uncover_node(node):
                if self.up[node]:    self.down[self.up[node]] = node
                if self.down[node]:  self.up[self.down[node]] = node
                if self.left[node]:  self.right[self.left[node]] = node
                if self.right[node]: self.left[self.right[node]] = node

            stack = history.pop()
            for current in stack[::-1]:
                uncover_node(current)
        
        solution = []
        solution_found = False

        def backtrack():
            nonlocal solution_found
            
            current = self.right[self.dummy_node]
            assert current != self.dummy_node

            if not current:
                solution_found = True
                return 
            
            current = self.down[current]
            while current:
                cover(current)
                solution.append(self.row_num[current])

                backtrack()
                if solution_found:
                    return

                uncover(current)

                current = self.down[current]
                solution.pop()

        backtrack()

        return solution_found, solution

    def visualize(self, filename):
        from graphviz import Digraph

        dot = Digraph(comment="Dancing Links Graph")
        dot.attr(rankdir="LR")
        
        rendered = set()
        def render_nodes(nodes):
            nonlocal rendered
            for node in nodes:
                if node not in rendered:
                    label = str(node.item) or "DUMMY" if isinstance(node, HeaderNode) else ""
                    dot.node(str(id(node)), label)

        render_nodes(self.left.keys())
        render_nodes(self.right.keys())
        render_nodes(self.up.keys())
        render_nodes(self.down.keys())
         
        def render_edges(edges, **attribs):
            for node1, node2 in edges.items():
                if node2:
                    dot.edge(str(id(node1)), str(id(node2)), **attribs)

        render_edges(self.right, color="green")
        render_edges(self.left,  color="red")
        render_edges(self.down,  color="magenta")
        render_edges(self.up,    color="blue")

        dot.render(filename, format='png', cleanup=True)
        print(f"Graph saved to {filename}.png")

def main(args):
    universe = args.universe
    sets = args.set

    print(f"Universe: {universe}")

    print("Sets:")
    for i, s in enumerate(sets):
        print(f"{i+1}: {s}")

    graph = Graph(universe, sets)
    if args.visualize:
        graph.visualize(args.visualize_filename)
    
    solution_found, solution = graph.solve()
    if solution_found:
        print(f"Solution indices: {solution}")
        solution_sets = [sets[i-1] for i in solution]
        print(f"Solution sets:    {solution_sets}")
    else:
        print("No solution found")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    def parse_set(string):
        try:
            return set(item.strip() for item in string.split(","))
        except ValueError:
            raise argparse.ArgumentTypeError(
                f"Invalid set format: \"{s}\". Use comma separated values"
            )

    parser.add_argument("universe", type=parse_set, help="The universe (eg: \"a, b, c\")")
    parser.add_argument("set", type=parse_set, nargs="+", help="List of sets (eg: \"a, c\" \"b\")")
    parser.add_argument("--visualize", action="store_true", help="Enable graph visualization with Graphviz")
    parser.add_argument("--visualize_filename", type=str, default="dlx_graph", help="Filename (without extension) for the visualization output")

    args = parser.parse_args()

    main(args)

