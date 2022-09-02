import java.util.ArrayList;
public class Node {

    // Fields:
    int value;
    Node next;
    Node prev;

    // Constructor: used for creating objects
    public Node(int v) {

        this.value = v;
    }


    private void changeValue(int v) {
        // A bunch of code here
        System.out.println("CAME TO CHANGE VALUES");
        this.value = v;
    }

    public static void main(String args[]) {
        ArrayList<Integer> arr[] = new ArrayList[5];
        Node n = new Node(5);
        arr[0] = n;
        System.out.println(n.value);
        n.value = 10;
        n.changeValue(10);
        System.out.println(n.value);
    }

}