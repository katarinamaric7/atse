class BubbleSort:
    @staticmethod
    def sort(array):
        n = len(array)

        for i in range(n - 1):
            swapped = False

            for j in range(n - i - 1):
                if array[j] > array[j + 1]:
                    array[j], array[j + 1] = array[j + 1], array[j]
                    swapped = True

            if not swapped:
                break

    @staticmethod
    def sort_basic(array):
        n = len(array)

        for i in range(n - 1):
            for j in range(n - i - 1):
                if array[j] > array[j + 1]:
                    array[j], array[j + 1] = array[j + 1], array[j]
