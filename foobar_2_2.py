def solution(h, q):
    # Get labels
    tree_size = (2 ** h) - 1
    post_order_labels = list(range(1, tree_size + 1))

    # Construct post-order tree
    post_order_tree = construct_postorder_tree(h, 1, post_order_labels)

    # Identify parent nodes for items in q
    parent_nodes = []
    for i in q:
        parent = find_parent_node(post_order_tree, -1, i) or -1
        parent_nodes.append(parent)

    return parent_nodes

class Node:
    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right

def find_parent_node(tree, parent, i):
    # Finds the value of the parent node in tree t to a node with value i
    # tree : Node = tree to traverse in search of value i
    # parent : int = value of the current parent node
    # i : int = value we are searching for within the tree
    # rtype : int

    # If we have traversed to the end of the tree without finding the desired value, return None
    if tree is None:
        return None

    # If we have found the desired value, return the current parent
    if tree.data == i:
        return parent

    # Otherwise, traverse the trees to the left and right of the current node
    val_l = find_parent_node(tree.left, tree.data, i)
    val_r = find_parent_node(tree.right, tree.data, i)

    # Otherwise, returns whichever of val_l or val_r is not None
    # If value i is not to be found in either subtree, returns None
    return val_l or val_r

def construct_postorder_tree(h, lvl, vals):
    # Constructs a perfect binary tree of height h and values vals
    # Construction is done recursively
    # h : int = number of levels of the complete tree
    # lvl : int = current level/tier of the tree under construction (starting at 1)
    # vals : list[int] = list of values from which to construct the tree
    # rtype : Node
    if h == lvl:
        tree = Node(vals.pop(0), None, None)
        return tree
    else:
        tree = Node(None,
                    construct_postorder_tree(h, lvl + 1, vals),
                    construct_postorder_tree(h, lvl + 1, vals),
                    )
        tree.data = vals.pop(0)

    return tree

def preorder_tree(tree_node):
    # Extra tree traversal method
    # Returns a list of tree values from preorder traversal
    l = [tree_node.data]

    if tree_node.left is not None:
        l.extend(preorder_tree(tree_node.left))
    if tree_node.right is not None:
        l.extend(preorder_tree(tree_node.right))

    return l

def inorder_tree(tree_node):
    # Extra tree traversal method
    # Returns a list of tree values from inorder traversal
    if tree_node.left is None:
        l = [tree_node.data]
    else:
        l = inorder_tree(tree_node.left)
        l.append(tree_node.data)
        if tree_node.right is not None:
            l.extend(inorder_tree(tree_node.right))

    return l


if __name__ == '__main__':
    print(solution(3, [1, 4, 7]))
    print(solution(3, [7, 3, 5, 1]))
    print(solution(5, [19, 14, 28]))
