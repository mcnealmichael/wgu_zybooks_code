from LAB_AVLTree.AVLNode import AVLNode

class AVLPrint:
    @staticmethod
    def indent_lines(lines, number_of_spaces):
        if number_of_spaces <= 0:
            return
        # Prepend indentation to each line
        indent = " " * number_of_spaces
        for i in range(len(lines)):
            lines[i] = indent + lines[i]

    @staticmethod
    def tree_to_lines(subtree_root):
        result = []
        if subtree_root == None:
            return result

        # Make a string with the subtree_root's key enclosed in brackets
        root_string = f"[{subtree_root.get_key()}]"
        root_str_len = len(root_string)

        # Case 1: subtree_root is a leaf
        if subtree_root.get_left() == None and subtree_root.get_right() == None:
            result.append(root_string)
            return result

        # Recursively make line strings for each child
        left_lines = AVLPrint.tree_to_lines(subtree_root.get_left())
        right_lines = AVLPrint.tree_to_lines(subtree_root.get_right())

        line_count = max(len(left_lines), len(right_lines))
        all_lines = [""] * (line_count + 2)

        # Case 2: subtree_root has no left child
        if subtree_root.get_left() == None:
            # Create the first 2 lines, not yet indented
            all_lines[0] = root_string
            all_lines[1] = (" " * root_str_len) + "\\"

            # Find where the right child starts
            right_child_indent = right_lines[0].find("[")

            # Goal: Indent lines appropriately so that the parent's right
            # branch character ('\') matches up with the right child's '['.
            
            if right_child_indent <= root_str_len:
                # Indent all lines below
                num_spaces = root_str_len - right_child_indent
                AVLPrint.indent_lines(right_lines, num_spaces)
            else:
                # Indent first 2 lines
                indent = " " * (right_child_indent - root_str_len)
                all_lines[0] = indent + all_lines[0]
                all_lines[1] = indent + all_lines[1]

            # Copy right_lines into all_lines starting at index 2
            for i in range(len(right_lines)):
                all_lines[i + 2] = right_lines[i]

            return all_lines

        # Case 3: subtree_root has no right child
        if subtree_root.get_right() == None:
            # Goal: Indent lines appropriately so that the parent's left
            # branch character ('/') matches up with the left child's ']'.

            # Create the first 2 lines
            indent = " " * left_lines[0].find("]")
            all_lines[0] = indent + " " + root_string
            all_lines[1] = indent + "/"

            # Copy left_lines into all_lines starting at index 2
            for i in range(len(left_lines)):
                all_lines[i + 2] = left_lines[i]

            return all_lines

        # Case 4: subtree_root has both a left and right child

        # The goal is to have the two child nodes as close to the parent as
        # possible without overlap on any level.

        # Compute absolute indentation, in number of spaces, needed for right
        # lines
        indent_needed = 0
        if len(right_lines) > 0:
            # Indent should at least get the immediate right child to be to the
            # right of the root
            indent_needed = max(0,
                                (len(left_lines[0]) + len(root_string)) -
                                right_lines[0].find("["))

        for i in range(0, min(len(left_lines), len(right_lines)), 2):
            # Lines with branches are skipped, so the line of interest has only
            # nodes.  The difference between where the left line ends and the
            # right line begins should be at least 3 spaces for clarity.
            right_begin = right_lines[i].find("[")

            for_this_line = len(left_lines[i]) + 3 - right_begin
            indent_needed = max(indent_needed, for_this_line)

        # Build final lines in allLines starting at index 2
        absolute_indent = " " * indent_needed
        for i in range(max(len(left_lines), len(right_lines))):
            # If no right line, just take the left
            if i >= len(right_lines):
                all_lines[2 + i] = left_lines[i]
            else:
                left = ""
                if i < len(left_lines):
                    left = left_lines[i]
                right = absolute_indent + right_lines[i]
                all_lines[2 + i] = left + right[len(left):]

        # The first 2 lines remain.  AllLines[2] has the proper string for the
        # 2 child nodes, and so can be used to create branches in all_lines[1].
        left_index = all_lines[2].find("]")
        right_index = all_lines[2].rfind("[")
        all_lines[1] = (" " * left_index) + "/" + (" " * (right_index - left_index - 1)) + "\\"

        # The space between left_index and right_index is the space that
        # subtree_root's string should occupy.  If root_string is too short, put
        # underscores on the sides.
        root_str_len = right_index - left_index - 1
        if len(root_string) < root_str_len:
            difference = root_str_len - len(root_string)
            underscores = "_" * (difference // 2)
            if 0 == difference % 2:
                root_string = underscores + root_string + underscores
            else:
                root_string = underscores + root_string + underscores + "_"

        all_lines[0] = (" " * (left_index + 1)) + root_string
        return all_lines

    @staticmethod
    def tree_to_string(subtree_root):
        if subtree_root == None:
            return "(empty tree)"

        # First convert the tree to a vector of line strings
        lines = AVLPrint.tree_to_lines(subtree_root)

        # Combine all lines into one string
        tree_string = lines[0]
        for i in range(1, len(lines)):
            tree_string += ("\n" + lines[i])

        return tree_string