package general;

public abstract class BinarySearchTree {

    /*
    Fields and constructors
     */

    protected Node root;

    protected int size;


    /*
    Public methods
     */
    public abstract Node createNode(Integer value, Node parent, Node left, Node right);

    public Node search(int value) {
        Node node = root;
        while (node != null && node.getValue() != null && !node.getValue().equals(value)) {
            if (value < node.getValue()) {
                node = node.getLeft();
            } else {
                node = node.getRight();
            }
        }

        return node;
    }

    public Node insert(int value) {
        if (root == null) {
            root = createNode(value, null, root, null);
            size++;
            return root;
        }

        Node insertParentNode = null;
        Node tempNode = root;

        while (tempNode != null & tempNode.getValue() != null) {
            insertParentNode = tempNode;
            if (value < tempNode.getValue()) {
                tempNode = tempNode.getLeft();
            } else {
                tempNode = tempNode.getRight();
            }
        }

        Node newNode = createNode(value, insertParentNode, null, null);
        if (insertParentNode.getValue() > newNode.getValue()) {
            insertParentNode.setLeft(newNode);
        } else {
            insertParentNode.setRight(newNode);
        }
        size++;
        return newNode;
    }

    public Node delete(Integer value) {
        Node deletedNode = search(value);
        if (deletedNode == null) {
            return null;
        } else {
           return delete(deletedNode);
        }
    }

    public Boolean contains(Integer value) {
        return search(value) != null;
    }

    public void printTree() {

    }

    /*
    Protected methods
     */

    protected Node delete(Node node) {
        if (node != null) {
            Node nodeToReturn = null;
            if (node.getLeft() == null) {
                nodeToReturn = transplant(node, node.getRight());
            } else if (node.getRight() == null) {
                nodeToReturn = transplant(node, node.getLeft());
            } else {
                Node successorNode = getMinimum(node.getRight());
                if (successorNode.getParent() != node) {
                    transplant(successorNode, node.getRight());
                    successorNode.setRight(node.getRight());
                    successorNode.getRight().setParent(successorNode);
                }
                transplant(node, successorNode);
                successorNode.setLeft(node.getLeft());
                successorNode.getLeft().setParent(successorNode);
                nodeToReturn = successorNode;
            }
            size--;
            return nodeToReturn;
        }
        return null;
    }

    /*
    Puts one node from tree to the place of nodeToReplace
     */
    protected Node transplant(Node nodeToReplace, Node newNode) {
        if (nodeToReplace.getParent() == null) {
            this.root = newNode;
        } else if (nodeToReplace == nodeToReplace.getParent().getLeft()) {
            nodeToReplace.getParent().setLeft(newNode);
        } else {
            nodeToReplace.getParent().setRight(newNode);
        }

        if (newNode != null) {
            newNode.setParent(nodeToReplace.getParent());
        }

        return newNode;
    }

    protected Node getMinimum(Node node) {
        while (node.getLeft() != null) {
            node = node.getLeft();
        }
        return node;
    }

    protected Node getMaximum(Node node) {
        while (node.getRight() != null) {
            node = node.getRight();
        }
        return node;
    }
}
