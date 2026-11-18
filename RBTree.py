from RBTNode import RBTNode

class RBTree:
    # Constructor to create an RBTree
    def __init__(self):
        pass

    def insert_node(self, node):
        # Begin with normal BST insertion
        if self.root == None:
            self.root = node
        else:
            current_node = self.root
            while current_node != None:
                if node.get_key() < current_node.get_key():
                    if current_node.get_left() == None:
                        current_node.set_left(node)
                        break
                    else:
                        current_node = current_node.get_left()
                else:
                    if current_node.get_right() == None:
                        current_node.set_right(node)
                        break
                    else:
                        current_node = current_node.get_right()

        # Color the node red, then balance
        node.set_color(RBTNode.RED_COLOR)
        self.insertion_balance(node)

    def insert_key(self, key):
        if self.contains(key):
            return False

        new_node = RBTNode(key, None, True)
        self.insert_node(new_node)
        return True

    # Performs a left rotation at the given node
    def rotate_left(self, node):
        # Get the right child's left child
        right_left_child = node.get_right().get_left()

        # Step 1 - the right child moves up to the node's position.
        # node is detached from the tree and reattached later.
        if node.get_parent() != None:
            node.get_parent().replace_child(node, node.get_right())
        else: # node is root
            self.root = node.get_right()
            self.root.set_parent_to_none()

        # Step 2 - node becomes the left child of the node's right child
        # temporarily detaching right_left_child from the tree
        node.get_right().set_left(node)

        # Step 3 - right_left_child is reattached as the right child of node
        node.set_right(right_left_child)

    # Rotates right
    def rotate_right(self, node):
        left_right_child = node.get_left().get_right()
        if node.get_parent() != None:
            node.get_parent().replace_child(node, node.get_left())
        else: # node is root
            self.root = node.get_left()
            self.root.set_parent_to_none()

        node.get_left().set_right(node)
        node.set_left(left_right_child)

    def insertion_balance(self, node):
        parent = node.get_parent()
        grandparent = node.get_grandparent()
        uncle = node.get_uncle()

        if parent == None:
            node.set_color(RBTNode.BLACK_COLOR)
            return

        if parent.is_black():
            return

        if uncle != None and uncle.is_red():
            uncle.set_color(RBTNode.BLACK_COLOR)
            parent.set_color(RBTNode.BLACK_COLOR)
            grandparent.set_color(RBTNode.RED_COLOR)
            self.insertion_balance(grandparent)
            return

        if node is parent.get_right() and parent is grandparent.get_left():
            self.rotate_left(parent)
            node = parent
            parent = node.get_parent()

        elif node is parent.get_left() and parent is grandparent.get_right():
            self.rotate_right(parent)
            node = parent
            parent = node.get_parent()

        parent.set_color(RBTNode.BLACK_COLOR)
        grandparent.set_color(RBTNode.RED_COLOR)
        if node is parent.get_left():
            self.rotate_right(grandparent)
        else:
            self.rotate_left(grandparent)