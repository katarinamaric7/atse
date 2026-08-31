class SelectionSort:
    @staticmethod
    def selection_sort(arr):
        n = len(arr)
        for i in range(n - 1):
            min_index = i
            for j in range(i + 1, n):
                if arr[j] < arr[min_index]:
                    min_index = j
            arr[i], arr[min_index] = arr[min_index], arr[i]

    @staticmethod
    def improved_selection_sort(arr):
        n = len(arr)
        for i in range(n - 1):
            min_index = i
            for j in range(i + 1, n):
                if arr[j] < arr[min_index]:
                    min_index = j

            min_value = arr[min_index]
            while min_index > i:
                arr[min_index] = arr[min_index - 1]
                min_index -= 1
            arr[i] = min_value