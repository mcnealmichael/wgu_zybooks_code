class AVLNode:
    def __init__(self, node_key):
        self.key = node_key
        self.parent = None
        self.left = None
        self.right = None
        self.height = 0

    # Calculates this node's balance factor, defined as:
    # height(left subtree) - height(right subtree)
    def get_balance(self):
        # Get current height of left subtree, or -1 if None
        left_height = -1
        if self.left != None:
            left_height = self.left.height

        # Get current height of right subtree, or -1 if None
        right_height = -1
        if self.right != None:
            right_height = self.right.height

        # Calculate the balance factor
        return left_height - right_height

    # Returns this node's key
    def get_key(self):
        return self.key

    # Returns this node's left child node
    def get_left(self):
        return self.left

    # Returns this node's right child node
    def get_right(self):
        return self.right

    # Returns this node's parent
    def get_parent(self):
        return self.parent

    # Replaces a current child with a new child. Determines if the current
    # child is the left or right, then calls set_left() or set right() with
    # new node appropriately.  Returns True if the new child is assigned, False
    # otherwise.
    def replace_child(self, current_child, new_child):
        if self.left is current_child:
            self.set_left(new_child)
            return True
        elif self.right is current_child:
            self.set_right(new_child)
            return True

        # current_child is not a child of this node
        return False

    # Reassigns this node's key with the new key
    def set_key(self, new_key):
        self.key = new_key

    # Reassigns this node's left child with the new child.  If not None, the
    # new left child's parent is assigned with this node.  After assigning the
    # new child, this node's height is updated
    def set_left(self, new_left_child):
        # Assign new left child
        self.left = new_left_child

        # if the new child is non-null, assign parent
        if self.left != None:
            self.left.parent = self

        # A new child may change this node's height, so call update_height()
        self.update_height()

    # Reassigns this node's parent node with the new parent
    def set_parent(self, new_parent):
        self.parent = new_parent

    # Reassigns this node's right child with the new child.  If not None, the
    # new right child's parent is assigned with this node.  After assigned the
    # new child, this node's height is updated
    def set_right(self, new_right_child):
        # Assign new right child
        self.right = new_right_child

        # if the new child is not None, assign parent
        if self.right != None:
            self.right.parent = self

        # A new child may change this node's height, so call update_height()
        self.update_height()

    # Recalculates the current height of the subtree rooted at this node
    # Usually called after a subtree has been modified.
    def update_height(self):
        # Get current height or left subtree, or -1 if None
        left_height = -1
        if self.left != None:
            left_height = self.left.height

        # Get current height of right subtree, or -1 if None
        right_height = -1
        if self.right != None:
            right_height = self.right.height

        # Assign height with calculated node height.
        self.height = max(left_height, right_height) + 1