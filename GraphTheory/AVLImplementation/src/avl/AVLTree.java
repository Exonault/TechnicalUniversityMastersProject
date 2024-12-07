package avl;

import general.Node;
import general.SelfBalancingBinarySearchTree;

public class AVLTree extends SelfBalancingBinarySearchTree {
    @Override
    public Node createNode(Integer value, Node parent, Node left, Node right) {
        return new AVLNode(value, parent, left, right);
    }
}
