package avl;

import general.Node;

public class AVLNode extends Node
{
    private Integer height;

    public AVLNode(Integer value, Node left, Node right, Node parent) {
        super(value, left, right, parent);
    }

    public Integer getHeight() {
        return height;
    }

    public void setHeight(Integer height) {
        this.height = height;
    }
}
