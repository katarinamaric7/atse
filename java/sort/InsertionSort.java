package sort;

public class InsertionSort {

    public void sort(int[] array) {

        for (int i = 1; i < array.length; i++) {

            int key = array[i];
            int j = i - 1;

            while (j >= 0) {

                if (array[j] > key) {
                    array[j + 1] = array[j];
                    j--;
                } else {
                    break;
                }
            }

            array[j + 1] = key;
        }
    }

    public void recursiveSort(int[] array) {

        recursiveSort(array, array.length);
    }

    //Pomoćna metoda za rekurzivno sortiranje prvih n elemenata.
    private void recursiveSort(int[] array, int n) {

        if (n <= 1) {
            return;
        }

        recursiveSort(array, n - 1);

        int key = array[n - 1];
        int j = n - 2;

        while (j >= 0) {

            if (array[j] > key) {
                array[j + 1] = array[j];
                j--;
            } else {
                break;
            }
        }

        array[j + 1] = key;
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