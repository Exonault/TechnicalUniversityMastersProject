package general;

public class Node {

    public Integer value;
    public Node parent;
    public Node left;
    public Node right;

    public Node(Integer value, Node parent, Node left, Node right) {
        super();
        this.value = value;
        this.parent = parent;
        this.left = left;
        this.right = right;
    }

    @Override
    public int hashCode() {
        final int prime = 31;
        int result = 1;
        result = prime * result + ((value == null) ? 0 : value.hashCode());
        return result;
    }

    @Override
    public boolean equals(Object obj) {
        if (this == obj)
            return true;
        if (obj == null)
            return false;
        if (getClass() != obj.getClass())
            return false;
        Node other = (Node) obj;
        if (value == null) {
            return other.value == null;
        } else
            return value.equals(other.value);
    }

}
