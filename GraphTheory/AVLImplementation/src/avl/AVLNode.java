package avl;

import general.Node;


public class AVLNode extends Node {
    public int height;

    public AVLNode(int value, Node parent, Node left, Node right) {
        super(value, parent, left, right);
    }
}

