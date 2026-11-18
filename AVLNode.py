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
    # new node appropriately.  Returns True if the new child is assigned, Fales
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
    # new right child's parent is assigned with this node.  After assigne the
    # new child, this node's height is updated
    def set_right(self, new_right_child):
        # Assigne new right child
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

        # Assigne height with calculated node height.
        self.height = max(left_height, right_height) + 1

    def rotate_right(self, node):
        # Get references to the node's parent, leftchild, and left child's
        # right child
        parent = node.get_parent()
        left_child = node.get_left()
        left_right_child = left_child.get_right()

        # First reassign node's left child
        node.set_left(left_right_child)

        # Next, reassign former left child's right child
        left_child.set_right(node)

        # Lastly, replace parent's child or reassign root if parent is None
        if parent != None:
            parent.replace_child(node, left_child)
        else:
            self.root = left_child
            self.root.set_parent(None)

    def rebalance(self, node):
        # First update the node's height
        node.update_height()

        # Check for an imbalance
        if node.get_balance() == -2:
            # The subtree is too big to the right
            if node.get_right().get_balance() == 1:
                # Double rotation case.  First do a right rotation on the right
                # child.
                self.rotate_right(node.get_right())
            # A left rotation will now make the subtree balanced
            self.rotate_left(node)
        elif node.get_balance() == 2:
            # The subtree is too big to the left
            if node.get_left().get_balance() == -1:
                # Double rotation case.  First do a left rotation on the left
                # child.
                self.rotate_left(node.get_left())
            # A right rotation will now make the subtree balanced
            self.rotate_right(node)

    def insert_key(self, key):
        if self.contains(key):
            return False
        self.insert_node(AVLNode(key))
        return True

    def insert_node(self, node):
        # Check if tree is empty
        if self.root == None:
            self.root = node
        else:
            # Step 1 - do a regular binary search tree insert
            current_node = self.root
            while current_node != None:
                # Choose to go left or right
                if node.get_key() < current_node.get_key():
                    # Go left.  If left child is None, insert new node here.
                    if current_node.get_left() == None:
                        current_node.set_left(node)
                        current_node = None
                    else:
                        # Go left and continue loop
                        current_node = current_node.get_left()
                else:
                    # Go right. If right child None, insert new node here.
                    if current_node.get_right() == None:
                        current_node.set_right(node)
                        current_node = None
                    else:
                        # Go right and continue loop
                        current_node = current_node.get_right()
            # Step 2 - Rebalance along path from the new node's parent up to
            # the root
            node = node.get_parent()
            while node != None:
                self.rebalance(node)
                node = node.get_parent()  

    def remove_key(self, key):
        node = self.search(key)
        if node == None:
            return False
        return self.remove_node(node)

    def remove_node(self, node_to_remove):
        # Base-case:
        if node_to_remove == None:
            return False

        # node_to_remove's parent is needed for rebalancing 
        parent = node_to_remove.get_parent()

        # Case 1: Internal node with 2 children
        if node_to_remove.get_left() != None and node_to_remove.get_right() != None:
            # Find successor
            successor_node = node_to_remove.get_right()
            while successor_node.get_left() != None:
                successor_node = successor_node.get_left()

            # Copy the value from the node
            node_to_remove.set_key(successor_node.get_key())

            # Recursively remove successor
            self.remove_node(successor_node)

            # Nothing left to do since the recursive all will have rebalanced
            return True

        # Case 2: Root node (with 1 or 0 children)
        elif node_to_remove is self.root:
            if node_to_remove.get_left() != None:
                self.root = node_to_remove.get_left()
            else:
                self.root = node_to_remove.get_right()

            if self.root != None:
                self.root.set_parent(None)

            return True

        # Case 3: Internal with left child only
        elif node_to_remove.get_left() != None:
            parent.replace_child(node_to_remove, node_to_remove.get_left())

        # Case 4: Internal with right child only OR leaf
        else:
            parent.replace_child(node_to_remove, node_to_remove.get_right())

        # Anything that was below node_to_remove that has persisted is already
        # correctly balanced, but ancestors of node_to_remove may need
        # rebalancing
        node_to_rebalance = parent
        while node_to_rebalance != None:
            self.rebalance(node_to_rebalance)
            node_to_rebalance = node_to_rebalance.get_parent()

        return True