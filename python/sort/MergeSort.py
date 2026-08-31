class MergeSort:
    @staticmethod
    def mergeSort(arr):
        if len(arr) <= 1:
            return arr

        mid = len(arr) // 2
        leftHalf = arr[:mid]
        rightHalf = arr[mid:]

        sortedLeft = MergeSort.mergeSort(leftHalf)
        sortedRight = MergeSort.mergeSort(rightHalf)

        return MergeSort.merge(sortedLeft, sortedRight)

    @staticmethod
    def merge(left, right):
        result = []
        i = j = 0

        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

        result.extend(left[i:])
        result.extend(right[j:])

        return result
    

    @staticmethod
    def mergeSortWithoutRecursion(arr):
        step = 1  
        length = len(arr)
        
        while step < length:
            for i in range(0, length, 2 * step):
                left = arr[i:i + step]
                right = arr[i + step:i + 2 * step]
                
                merged = MergeSort.merge(left, right)
                
                for j, val in enumerate(merged):
                    arr[i + j] = val
                    
            step *= 2 
            
        return arr