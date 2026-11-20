from LAB_AVLTree.AVLTree import AVLTree
from ExtendedAVLNode import ExtendedAVLNode

class ExtendedAVLTree(AVLTree):
    def __init__(self):
        super().__init__()

    # Each node in an ExtendedAVLTree is an ExtendedAVLNode
    def make_new_node(self, key):
        return ExtendedAVLNode(key)

    def insert_node(self, node):
        current_node = node
        super().insert_node(node)

        while current_node != None:
            current_node.update_subtree_key_count()
            current_node = current_node.get_parent()

    def get_nth_key(self, n):
        # Start at the root 
        current_node = self.root

        # Start by getting the size of the left side key count
        left_size = self.get_left().get_subtree_key_count()

        while current_node != None:
            # compare n to the size of the left subtree
            if n < left_size:
                current_node = self.get_left()
            elif n == left_size:
                return current_node
            else:
                n = n - left_size - 1
                current_node = self.get_right()

        return None