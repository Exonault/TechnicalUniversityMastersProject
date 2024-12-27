import avl.AVLTree;

import java.util.Random;

public class Main {
    public static void main(String[] args) {
        AVLTree tree = new AVLTree();
        Random rand = new Random(42);
        for (int i = 0; i < 15; i++) {
            int i1 = rand.nextInt(15);
            if (!tree.contains(i1)) {
                tree.insert(i1);
                System.out.println("Inserted: " + i1);
                tree.printTree();
                System.out.println();
            }
        }

    }
}