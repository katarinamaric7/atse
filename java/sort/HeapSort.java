package sort;

public class HeapSort {

    public static void sort(int[] array) {
        int n = array.length;

        for (int i = n / 2 - 1; i >= 0; i--) {
            heapifyIterative(array, n, i);
        }

        for (int i = n - 1; i > 0; i--) {
            int temp = array[0];
            array[0] = array[i];
            array[i] = temp;
            heapifyIterative(array, i, 0);
        }
    }

    private static void heapifyIterative(int[] array, int size, int root) {
        while (true) {
            int largest = root;
            int left = 2 * root + 1;
            int right = 2 * root + 2;

            if (left < size && array[left] > array[largest]) largest = left;
            if (right < size && array[right] > array[largest]) largest = right;

            if (largest == root) break;

            int swap = array[root];
            array[root] = array[largest];
            array[largest] = swap;
            root = largest;
        }
    }

    public static void sortRecursive(int[] array) {
        int n = array.length;

        for (int i = n / 2 - 1; i >= 0; i--) {
            heapifyRecursive(array, n, i);
        }

        for (int i = n - 1; i > 0; i--) {
            int temp = array[0];
            array[0] = array[i];
            array[i] = temp;
            heapifyRecursive(array, i, 0);
        }
    }

    private static void heapifyRecursive(int[] array, int size, int root) {
        int largest = root;
        int left = 2 * root + 1;
        int right = 2 * root + 2;

        if (left < size && array[left] > array[largest]) largest = left;
        if (right < size && array[right] > array[largest]) largest = right;

        if (largest != root) {
            int swap = array[root];
            array[root] = array[largest];
            array[largest] = swap;
            heapifyRecursive(array, size, largest);
        }
    }
}
