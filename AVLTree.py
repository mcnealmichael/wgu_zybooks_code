from AVLNode import AVLNode
from AVLPrint import AVLPrint

class AVLTree:
    def __init__(self):
        self.root = None

    def contains(self, key):
        return self.search(key) != None
    
    def get_root(self):
        return self.root

    def print_tree(self, end = ""):
        print(f"{AVLPrint.tree_to_string(self.root)}{end}", end="")

    # Searches for a node with a matching key.  Returns the node with the
    # matching key, or None if no matching key exists in the tree
    def search(self, desired_key):
        current_node = self.root
        while current_node != None:
            # Return the node if the key matches
            if current_node.get_key() == desired_key:
                return current_node

            # Navigate to the left if the search key is < the node's key
            elif desired_key < current_node.get_key():
                current_node = current_node.get_left()

            # Navigate to the right if the search key is > the node's key
            else:
                current_node = current_node.get_right()

        # The key was not found in the tree
        return None

    # Performs a left rotation at the given node
    def rotate_left(self, node):
        # Get references to the node's parent, right child, and right child's
        # left child
        parent = node.get_parent()
        right_child = node.get_right()
        right_left_child = right_child.get_left()

        # First reassign node's right child
        node.set_right(right_left_child)

        # Next, reassign former right child's left child
        right_child.set_left(node)

        # Lastly, replace parent's child or reassign root if parent is None
        if parent != None:
            parent.replace_child(node, right_child)
        else:
            self.root = right_child
            self.root.set_parent(None)

    # Performs a right rotation at the given node
    def rotate_right(self, node):
        # Get references to the node's parent, left child, and left child's
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
