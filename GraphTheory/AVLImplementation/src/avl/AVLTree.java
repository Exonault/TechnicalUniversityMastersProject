package avl;

import general.Node;
import general.SelfBalancingBinarySearchTree;

public class AVLTree extends SelfBalancingBinarySearchTree {

    /*
    public methods
     */
    @Override
    public Node insert(int value) {
        Node newNode = super.insert(value);
        rebalance((AVLNode) newNode);
        return newNode;
    }

    @Override
    public Node delete(Integer element) {
        Node deleteNode = super.delete(element);
        if (deleteNode != null) {
            Node sucessorNode = super.delete(deleteNode);
            if (sucessorNode != null) {
                AVLNode minimum = sucessorNode.getRight() != null ? (AVLNode) getMinimum(sucessorNode.getRight()) : (AVLNode) sucessorNode;
                recomputeHeight(minimum);
                rebalance(minimum);
            } else {
                AVLNode node = (AVLNode) deleteNode.getParent();
                recomputeHeight(node);
                rebalance(node);
            }
            return sucessorNode;
        }
        return null;
    }

    @Override
    public Node createNode(Integer value, Node parent, Node left, Node right) {
        return new AVLNode(value, parent, left, right);
    }

    /*
    private methods
     */
    private void recomputeHeight(AVLNode node) {
        while (node != null) {
            node.setHeight(maxHeight((AVLNode) node.getLeft(), (AVLNode) node.getRight()) + 1);
            node = (AVLNode) node.getParent();
        }
    }

    private int maxHeight(AVLNode node1, AVLNode node2) {
        if (node1 != null && node2 != null) {
            return node1.getHeight() > node2.getHeight() ? node1.getHeight() : node2.getHeight();
        } else if (node1 == null) {
            return node2 != null ? node2.getHeight() : -1;
        } else if (node2 == null) {
            return node1 != null ? node1.getHeight() : -1;
        }

        return -1;
    }

    private void rebalance(AVLNode node) {
        while (node != null) {
            Node parent = node.getParent();
            int leftHeight = (node.getLeft() == null) ? -1 : ((AVLNode) node.getLeft()).getHeight();
            int rightHeight = (node.getRight() == null) ? -1 : ((AVLNode) node.getRight()).getHeight();
            int nodeBalance = rightHeight - leftHeight;

            // rebalance (-2 means left subtree outgrow, 2 means right subtree)
            if (nodeBalance == 2) {
                if (node.getRight().getRight() != null) {
                    node = (AVLNode) avlRotateLeft(node);
                    break;
                } else {
                    node = (AVLNode) doubleRotateRightLeft(node);
                    break;
                }
            } else if (nodeBalance == -2) {
                if (node.getLeft().getLeft() != null) {
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
        Node temp = super.rotateLeft(node);

        updateHeight((AVLNode) temp.getLeft());
        updateHeight((AVLNode) temp);

        return temp;
    }

    private Node avlRotateRight(Node node) {
        Node temp = super.rotateRight(node);

        updateHeight((AVLNode) temp.getRight());
        updateHeight((AVLNode) temp);

        return temp;
    }

    private Node doubleRotateRightLeft(Node node) {
        node.setRight(avlRotateRight(node.getRight()));
        return avlRotateLeft(node);
    }

    private Node doubleRotateLeftRight(Node node) {
        node.setLeft(avlRotateLeft(node.getLeft()));
        return avlRotateRight(node);
    }

    private void updateHeight(AVLNode node) {
        int leftHeight = (node.getLeft() == null) ? -1 : ((AVLNode) node.getLeft()).getHeight();
        int rightHeight = (node.getRight() == null) ? -1 : ((AVLNode) node.getRight()).getHeight();

        node.setHeight(Math.max(leftHeight, rightHeight));
    }

}
