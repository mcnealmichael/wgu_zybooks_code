class RBTNode:

    # Tracks if the node is red or black so the tree can stay balanced when
    # we add or remove nodes.
    RED_COLOR = 0
    BLACK_COLOR = 1

    # Constructor
    def __init__(self, node_key, parent_node, is_red, left_child = None, right_child = None):
        self.key = node_key
        self.parent = parent_node
        self.left = left_child
        self.right = right_child
        self.color = RBTNode.RED_COLOR if is_red else RBTNode.BLACK_COLOR

    # Replaces one of this node's children with a new child
    def replace_child(self, current_child, new_child):
        # Checks the left side and swaps
        if self.left is current_child:
            self.set_left(new_child)
            return True
        # Checks the right side and swaps
        elif self.right is current_child:
            self.set_right(new_child)
            return True
        return False # returns if no match for a child on either side

    # Reassigns this node's left child with the new child.  If not none, the
    # new left child's parent is assigned with this node.
    def set_left(self, new_child):
        self.left = new_child
        if self.left != None:
            self.left.parent = self

    # Reassigns this node's right child with the new child.  If not None, the
    # new right child's parent is assigned with this node.
    def set_right(self, new_child):
        self.right = new_child
        if self.right != None:
            self.right.parent = self

    def get_grandparent(self):
        if self.parent == None:
            return None
        return self.parent.parent

    def get_uncle(self):
        grandparent = self.get_grandparent()
        if grandparent == None:
            return None
        if grandparent.left is self.parent:
            return grandparent.right
        return grandparent.left
    