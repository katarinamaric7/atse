class QuickSort:

    def sort(self, array):

        self.__quick_sort(array, 0, len(array) - 1)

    def __quick_sort(self, array, low, high):

        if low >= high:
            return

        lt = low
        gt = high

        pivot = array[low]

        i = low + 1

        while i <= gt:

            if array[i] < pivot:

                self.__swap(array, lt, i)

                lt += 1
                i += 1

            elif array[i] > pivot:

                self.__swap(array, i, gt)
                gt -= 1

            else:
                i += 1

        self.__quick_sort(array, low, lt - 1)
        self.__quick_sort(array, gt + 1, high)

    def __swap(self, array, i, j):

        if i == j:
            return

        array[i], array[j] = array[j], array[i]

    @staticmethod
    def is_sorted(array):

        for i in range(1, len(array)):

            if array[i - 1] > array[i]:
                return False

        return True