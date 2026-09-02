class InsertionSort:

    def sort(self, array):

        for i in range(1, len(array)):

            key = array[i]
            j = i - 1

            while j >= 0:

                if array[j] > key:
                    array[j + 1] = array[j]
                    j -= 1
                else:
                    break

            array[j + 1] = key

    def recursive_sort(self, array, n=None):

        if n is None:
            n = len(array)

        if n <= 1:
            return

        self.recursive_sort(array, n - 1)
        key = array[n - 1]
        j = n - 2

        while j >= 0:

            if array[j] > key:
                array[j + 1] = array[j]
                j -= 1
            else:
                break

        array[j + 1] = key

    @staticmethod
    def is_sorted(array):

        for i in range(1, len(array)):
            if array[i - 1] > array[i]:
                return False

        return True