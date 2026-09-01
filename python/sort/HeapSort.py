class HeapSort:
    @staticmethod
    def sort(array):
        n = len(array)

        for i in range(n // 2 - 1, -1, -1):
            HeapSort._heapify_iterative(array, n, i)

        for i in range(n - 1, 0, -1):
            array[0], array[i] = array[i], array[0]
            HeapSort._heapify_iterative(array, i, 0)

    @staticmethod
    def _heapify_iterative(array, size, root):
        while True:
            largest = root
            left = 2 * root + 1
            right = 2 * root + 2

            if left < size and array[left] > array[largest]:
                largest = left
            if right < size and array[right] > array[largest]:
                largest = right

            if largest == root:
                break

            array[root], array[largest] = array[largest], array[root]
            root = largest

    @staticmethod
    def sort_recursive(array):
        n = len(array)

        for i in range(n // 2 - 1, -1, -1):
            HeapSort._heapify_recursive(array, n, i)

        for i in range(n - 1, 0, -1):
            array[0], array[i] = array[i], array[0]
            HeapSort._heapify_recursive(array, i, 0)

    @staticmethod
    def _heapify_recursive(array, size, root):
        largest = root
        left = 2 * root + 1
        right = 2 * root + 2

        if left < size and array[left] > array[largest]:
            largest = left
        if right < size and array[right] > array[largest]:
            largest = right

        if largest != root:
            array[root], array[largest] = array[largest], array[root]
            HeapSort._heapify_recursive(array, size, largest)
