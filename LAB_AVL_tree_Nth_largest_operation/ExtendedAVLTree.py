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

        while current_node != None:
            left_child = current_node.get_left()

            # Start by getting the size of the left side key count
            if left_child != None:
                left_size = left_child.get_subtree_key_count()
            else:
                left_size = 0

            # compare n to the size of the left subtree
            if n < left_size:
                current_node = left_child
            elif n == left_size:
                return current_node.get_key()
            else:
                n = n - left_size - 1
                current_node = current_node.get_right()

        return None

    def remove_node(self, node_to_remove):
        # Capture the parent before remove detaches the node
        parent = node_to_remove.get_parent()
        self.remove_AVLNode(node_to_remove)
        
        while parent != None:
            parent.update_subtree_key_count()
            parent = parent.get_parent()

    def rotate_left(self, node):
        super().rotate_left(node)
        # The node moved down and the new parent moved up
        node.update_subtree_key_count()
        if node.get_parent() != None:
            node.get_parent().update_subtree_key_count()

    def rotate_right(self, node):
        super().rotate_right(node)
        # The node moved down and the new parent moved up 
        node.update_subtree_key_count()
        if node.get_parent() != None:
            node.get_parent().update_subtree_key_count()