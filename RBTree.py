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

    def is_not_none_and_red(self, node):
        if node == None:
            return False
        return node.is_red()

    def is_none_or_black(self, node):
        if node == None:
            return True
        return node.is_black()

    def remove_key(self, key):
        node = self.search(key)
        if node != None:
            self.remove_node(node)
            return True
        return False

    def remove_node(self, node):
        if node.get_left() != None and node.get_right() != None:
            predecessor_node = node.get_predecessor()
            predecessor_key = predecessor_node.get_key()
            self.remove_node(predecessor_node)
            node.set_key(predecessor_key)
            return

        if node.is_black():
            self.prepare_for_removal(node)
        self.BST_remove(node.get_key())

        if self.root != None and self.root.is_red():
            self.root.set_color(RBTNode.BLACK_COLOR)

    def prepare_for_removal(self, node):
        if self.try_case1(node):
            return

        sibling = node.get_sibling()
        if self.try_case2(node, sibling):
            sibling = node.get_sibling()
        if self.try_case3(node, sibling):
            return
        if self.try_case4(node, sibling):
            return
        if self.try_case5(node, sibling):
            sibling = node.get_sibling()
        if self.try_case6(node, sibling):
            sibling = node.get_sibling()

        sibling.set_color(node.get_parent().get_color())
        node.get_parent().set_color(RBTNode.BLACK_COLOR)
        if node is node.get_parent().get_left():
            sibling.get_right().set_color(RBTNode.BLACK_COLOR)
            self.rotate_left(node.get_parent())
        else:
            sibling.get_left().set_color(RBTNode.BLACK_COLOR)
            self.rotate_right(node.get_parent())

    def try_case1(self, node):
        if node.is_red() or node.get_parent() == None:
            return True
        return False # not case 1

    def try_case2(self, node, sibling):
        if sibling.is_red():
            node.get_parent().set_color(RBTNode.RED_COLOR)
            sibling.set_color(RBTNode.BLACK_COLOR)
            if node is node.get_parent().get_left():
                self.rotate_left(node.get_parent())
            else:
                self.rotate_right(node.get_parent())
            return True
        return False # not case 2

    def try_case3(self, node, sibling):
        if node.get_parent().is_black() and sibling.are_both_children_black():
            sibling.set_color(RBTNode.RED_COLOR)
            self.prepare_for_removal(node.get_parent())
            return True
        return False # not case 3

    def try_case4(self, node, sibling):
        if node.get_parent().is_red() and sibling.are_both_children_black():
            node.get_parent().set_color(RBTNode.BLACK_COLOR)
            sibling.set_color(RBTNode.RED_COLOR)
            return True
        return False # not case 4

    def try_case5(self, node, sibling):
        if self.is_not_none_and_red(sibling.get_left()):
            if self.is_none_or_black(sibling.get_right()):
                if node is node.get_parent().get_left():
                    sibling.set_color(RBTNode.RED_COLOR)
                    sibling.get_left().set_color(RBTNode.BLACK_COLOR)
                    self.rotate_right(sibling)
                    return True
        return False # not case 5

    def try_case6(self, node, sibling):
        if self.is_none_or_black(sibling.get_left()):
            if self.is_not_none_and_red(sibling.get_right()):
                if node is node.get_parent().get_right():
                    sibling.set_color(RBTNode.RED_COLOR)
                    sibling.get_right().set_color(RBTNode.BLACK_COLOR)
                    self.rotate_left(sibling)
                    return True
        return False # not case 6