package avl;

import general.BinarySearchTree;
import general.Node;

public class AVLTree extends BinarySearchTree {

    @Override
    public Node insert(int element) {
        Node newNode = super.insert(element);
        balanceTree((AVLNode) newNode);
        return newNode;
    }

    @Override
    public Node delete(int element) {
        Node deleteNode = super.search(element);
        if (deleteNode != null) {
            Node successorNode = super.delete(deleteNode);
            if (successorNode != null) {
                AVLNode minimum = successorNode.right != null ? (AVLNode) getMinimum(successorNode.right) : (AVLNode) successorNode;
                recomputeHeight(minimum);
                balanceTree((AVLNode) minimum);
            } else {
                recomputeHeight((AVLNode) deleteNode.parent);
                balanceTree((AVLNode) deleteNode.parent);
            }
            return successorNode;
        }
        return null;
    }

    @Override
    protected Node createNode(int value, Node parent, Node left, Node right) {
        return new AVLNode(value, parent, left, right);
    }

    private void balanceTree(AVLNode node) {
        while (node != null) {
            Node parent = node.parent;

            int leftHeight = (node.left == null) ? -1 : ((AVLNode) node.left).height;
            int rightHeight = (node.right == null) ? -1 : ((AVLNode) node.right).height;
            int nodeBalance = rightHeight - leftHeight;

            if (nodeBalance == 2) { //  2 means right subtree overgrow
                assert node.right != null;
                if (node.right.right != null) {
                    node = (AVLNode) avlRotateLeft(node);
                    break;
                } else {
                    node = (AVLNode) doubleRotateRightLeft(node);
                    break;
                }
            } else if (nodeBalance == -2) { // -2 means left subtree overgrow
                assert node.left != null;
                if (node.left.left != null) {
                    node = (AVLNode) avlRotateRight(node);
                    break;
                } else {
                    node = (AVLNode) doubleRotateLeftRight(node);
                    break;
                }
            } else {
                updateHeight(node);
            }

            node = (AVLNode) parent;
        }
    }

    private Node avlRotateLeft(Node node) {
        Node temp = this.rotateLeft(node);

        updateHeight((AVLNode) temp.left);
        updateHeight((AVLNode) temp);
        return temp;
    }

    private Node avlRotateRight(Node node) {
        Node temp = this.rotateRight(node);

        updateHeight((AVLNode) temp.right);
        updateHeight((AVLNode) temp);
        return temp;
    }

    private Node doubleRotateRightLeft(Node node) {
        node.right = avlRotateRight(node.right);
        return avlRotateLeft(node);
    }

    private Node doubleRotateLeftRight(Node node) {
        node.left = avlRotateLeft(node.left);
        return avlRotateRight(node);
    }

    private void recomputeHeight(AVLNode node) {
        while (node != null) {
            node.height = maxHeight((AVLNode) node.left, (AVLNode) node.right) + 1;
            node = (AVLNode) node.parent;
        }
    }

    private int maxHeight(AVLNode node1, AVLNode node2) {
        if (node1 != null && node2 != null) {
            return Math.max(node1.height, node2.height);
        }
        if (node1 == null) {
            return node2 != null ? node2.height : -1;
        }
        if (node2 == null) {
            return node1 != null ? node1.height : -1;
        }
        return -1;
    }

    private void updateHeight(AVLNode node) {
        int leftHeight = (node.left == null) ? -1 : ((AVLNode) node.left).height;
        int rightHeight = (node.right == null) ? -1 : ((AVLNode) node.right).height;
        node.height = 1 + Math.max(leftHeight, rightHeight);
    }

    private Node rotateLeft(Node node) {
        Node temp = node.right;
        temp.parent = node.parent;

        node.right = temp.left;
        if (node.right != null) {
            node.right.parent = node;
        }

        temp.left = node;
        node.parent = temp;

        if (temp.parent != null) {
            if (node == temp.parent.left) {
                temp.parent.left = temp;
            } else {
                temp.parent.right = temp;
            }
        } else {
            root = temp;
        }

        return temp;
    }

    private Node rotateRight(Node node) {
        Node temp = node.left;
        temp.parent = node.parent;

        node.left = temp.right;
        if (node.left != null) {
            node.left.parent = node;
        }

        temp.right = node;
        node.parent = temp;

        if (temp.parent != null) {
            if (node == temp.parent.left) {
                temp.parent.left = temp;
            } else {
                temp.parent.right = temp;
            }
        } else {
            root = temp;
        }

        return temp;
    }
}
