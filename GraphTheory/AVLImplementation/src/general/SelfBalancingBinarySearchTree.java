package general;

public abstract class SelfBalancingBinarySearchTree extends BinarySearchTree {

    protected Node rotateLeft(Node node) {
        Node temp = node.getRight();
        temp.setParent(node.getParent());

        node.setRight(temp.getLeft());
        if (node.getRight() != null) {
            node.getRight().setParent(node);
        }

        temp.setLeft(node);
        node.setParent(temp);

        if (temp.getParent() != null) {
            if (node == temp.getParent().getLeft()) {
                temp.getParent().setLeft(temp);
            } else {
                temp.getParent().setRight(temp);
            }
        } else {
            root = temp;
        }

        return temp;
    }

    protected Node rotateRight(Node node) {
        Node temp = node.getLeft();
        temp.setParent(node.getParent());
        node.setLeft(temp.getRight());

        if (node.getLeft() != null) {
            node.getLeft().setParent(node);
        }

        temp.setRight(node);
        node.setParent(temp);

        if (temp.getParent() != null) {
            if (node == temp.getParent().getLeft()) {
                temp.getParent().setLeft(temp);
            } else {
                temp.getParent().setRight(temp);
            }
        } else {
            root = temp;
        }

        return temp;
    }

    public abstract Node delete(int element);
}
