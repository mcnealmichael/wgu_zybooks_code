from RBTNode import RBTNode
from RBTree import RBTree

# Declare keys to insert and keys to subsequently remove
keys_to_insert = [ 10, 20, 5, 22, 15, 47, 19, 3, 12, 18 ]
keys_to_remove = [
    12, # Removing 12 causes a right rotation at node 10
    20,
    30  # 30 is not in the tree, so remove_key() will return False
]
   
show_tree_after_each_insertion = False
   
# Create an empty RedBlackTree
tree = RBTree()

# Insert keys
for key in keys_to_insert:
    tree.insert_key(key)
    if show_tree_after_each_insertion:
        tree.print_tree(f"Tree after inserting {key}:\n", "\n\n")
      
# Print the tree after all inserts are complete
tree.print_tree("Tree after initial insertions:\n", "\n")
print()
   
# Remove keys
for key in keys_to_remove:
    if tree.remove_key(key):
        tree.print_tree(f"Removed key {key}:\n", "\n\n")
    else:
        print(f"Failed to remove key {key} (not found)")