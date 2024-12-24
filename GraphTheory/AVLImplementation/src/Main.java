import avl.AVLTree;

public class Main {
    public static void main(String[] args) {
        AVLTree tree = new AVLTree();
        for (int i = 1; i <= 15; i++) {
            tree.insert(i);
            tree.printTree();
            System.out.println();
        }

    }
}