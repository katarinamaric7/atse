package sort;

import java.util.ArrayDeque;
import java.util.Deque;

public class QuickSort {

    public void sort(int[] array) {
        quickSort(array, 0, array.length - 1);
    }

    // Rekurzivni QuickSort
    private void quickSort(int[] array, int low, int high) {

        if (low >= high)
            return;

        int lt = low;
        int gt = high;
        int pivot = array[low];
        int i = low + 1;

        while (i <= gt) {

            if (array[i] < pivot) {

                swap(array, lt, i);

                lt++;
                i++;

            } else if (array[i] > pivot) {

                swap(array, i, gt);
                gt--;

            } else {
                i++;
            }
        }

        quickSort(array, low, lt - 1);
        quickSort(array, gt + 1, high);
    }

    private void swap(int[] array, int i, int j) {

        if (i == j)
            return;

        int temp = array[i];
        array[i] = array[j];
        array[j] = temp;
    }

    public static boolean isSorted(int[] array) {

        for (int i = 1; i < array.length; i++) {

            if (array[i - 1] > array[i]) {
                return false;
            }
        }
        return true;
    }

    public static class IterativeQuickSort {

        public void sort(int[] array) {

            if (array == null || array.length < 2)
                return;

            Deque<Integer> stack = new ArrayDeque<>();

            stack.push(0);
            stack.push(array.length - 1);

            while (!stack.isEmpty()) {

                int high = stack.pop();
                int low = stack.pop();

                if (low >= high)
                    continue;

                int lt = low;
                int gt = high;
                int pivot = array[low];
                int i = low + 1;

                while (i <= gt) {

                    if (array[i] < pivot) {

                        swapStatic(array, lt, i);

                        lt++;
                        i++;

                    } else if (array[i] > pivot) {

                        swapStatic(array, i, gt);
                        gt--;

                    } else {
                        i++;
                    }
                }

                // Levi deo
                if (low < lt - 1) {
                    stack.push(low);
                    stack.push(lt - 1);
                }

                // Desni deo
                if (gt + 1 < high) {
                    stack.push(gt + 1);
                    stack.push(high);
                }
            }
        }

        private static void swapStatic(int[] array, int i, int j) {

            if (i == j)
                return;

            int temp = array[i];
            array[i] = array[j];
            array[j] = temp;
        }

        public static boolean isSorted(int[] array) {

            for (int i = 1; i < array.length; i++) {

                if (array[i - 1] > array[i]) {
                    return false;
                }
            }

            return true;
        }
    }
}
