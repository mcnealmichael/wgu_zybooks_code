from LAB_AVLTree.AVLNode import AVLNode

class ExtendedAVLNode(AVLNode):

    def __init__(self, node_key):
        super().__init__(node_key)
        self.subtree_key_count = 1

    def get_subtree_key_count(self):
        return self.subtree_key_count

    # Updates the count for the subtree rooted at this node
    def update_subtree_key_count(self):
        # ask the left child for its subtree count
        left_child = self.get_left()

        if left_child != None:
            left_count = left_child.get_subtree_key_count()
        else:
            left_count = 0

        # ask the right child for its subtree count
        right_child = self.get_right()

        if right_child != None:
            right_count = right_child.get_subtree_key_count()
        else:
            right_count = 0

        self.subtree_key_count = left_count + right_count + 1