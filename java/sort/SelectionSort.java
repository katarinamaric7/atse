package sort;

public class SelectionSort {

    public static void selection_sort(int[] arr) {
        int n = arr.length;

       for (int i = 0; i < n-1; i++) {
            int min_index = i;
            for (int j = i+1; j < n; j++) {
                if (arr[j] < arr[min_index]) {
                    min_index = j;
                }
            }
            int min_value = arr[min_index];
            for (int k = min_index; k > i; k--) {
                arr[k] = arr[k-1];
            }
            arr[i] = min_value;
        }
    }

    public static void improved_selection_sort(int[] arr) {
        int n = arr.length;

        for (int i = 0; i < n; i++) {
            int min_index = i;
            for (int j = i+1; j < n; j++) {
                if (arr[j] < arr[min_index]) {
                    min_index = j;
                }
            }
            int temp = arr[i];
            arr[i] = arr[min_index];
            arr[min_index] = temp;
        }

    }
}