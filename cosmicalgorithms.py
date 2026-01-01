'''Cosmic Core: Cosmic Algorithms
\n\tA library of essential algorithms, including searching and sorting algorithms.'''
from numpy import ndarray
__all__ = ['selectionsort', 'insertionsort', 'bubblesort', 'mergesort', 
           'quicksort', 'radixsort', 'linearsearch', 'binarysearch',
           'interpolationsearch']

#___Sorting Algorithms___
def selectionsort(data):
    '''Sort data using the selection sort algorithm.
    \nTime Complexity: O(n^2)'''
    if not hasattr(data, '__iter__'):
        raise TypeError('data must be an iterable')
    result = data.copy()
    if isinstance(result, ndarray):
        result = result.tolist()
    n = len(result)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if result[min_idx] > result[j]:
                min_idx = j
        result[i], result[min_idx] = result[min_idx], result[i]
    return result

def insertionsort(data):
    '''Sort data using the insertion sort algorithm.
    \nTime Complexity: O(n^2)'''
    if not hasattr(data, '__iter__'):
        raise TypeError('data must be an iterable')
    result = data.copy()
    if isinstance(result, ndarray):
        result = result.tolist()
    n = len(result)
    for i in range(1, n):
        key = result[i]
        j = i - 1
        while j >= 0 and key < result[j]:
            result[j + 1] = result[j]
            j -= 1
        result[j + 1] = key
    return result

def bubblesort(data):
    '''Sort data using the bubble sort algorithm.
    \nTime Complexity: O(n^2)'''
    if not hasattr(data, '__iter__'):
        raise TypeError('data must be an iterable')
    result = data.copy()
    if isinstance(result, ndarray):
        result = result.tolist()
    n = len(result)
    for i in range(n - 1):
        for j in range(n - i - 1):
            if result[j] > result[j + 1]:
                result[j], result[j + 1] = result[j + 1], result[j]
    return result

def mergesort(data):
    '''Sort data using the merge sort algorithm.
    \nTime Complexity: O(n log n)'''
    if not hasattr(data, '__iter__'):
        raise TypeError('data must be an iterable')
    result = data.copy()
    if isinstance(result, ndarray):
        result = result.tolist()

    if len(result) > 1:
        mid = len(result) // 2
        left_half = []
        right_half = []
        
        #Create left_half by iterating through data from head to mid
        for i in range(mid):
            left_half.append(result[i])

        #Create right_half by iterating from mid to tail
        for i in range(mid, len(result)):
            right_half.append(result[i])
        
        #Recursively call mergesort to sort the sub-lists
        left_half = mergesort(left_half)  #Get the sorted left_half
        right_half = mergesort(right_half)  #Get the sorted right_half

        i = j = k = 0
        while i < len(left_half) and j < len(right_half):
            if left_half[i] < right_half[j]:
                result[k] = left_half[i]
                i += 1
            else:
                result[k] = right_half[j]
                j += 1
            k += 1

        while i < len(left_half):
            result[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            result[k] = right_half[j]
            j += 1
            k += 1
    return result

def quicksort(data):
    '''Sort data using the quick sort algorithm (in-place).
    \nTime Complexity: O(n^2)'''
    if not hasattr(data, '__iter__'):
        raise TypeError('data must be an iterable')
    result = data.copy()
    if isinstance(result, ndarray):
        result = result.tolist()

    if len(result) > 1:
        pivot_index = len(result) // 2
        pivot = result[pivot_index]
        left = []
        middle = []
        right = []
        for i in range(len(result)):
            x = result[i]
            if x < pivot:
                left.append(x)
            elif x == pivot:
                middle.append(x)
            else:
                right.append(x)
        
        result.clear()
        result.extend(quicksort(left) + middle + quicksort(right)) 
    return result

def radixsort(data, base = 10):
    '''Sort data using the radix sort algorithm.
    \nTime Complexity: O(ω*n)
    \nPrecondition: all elements in the data are non-negative integers.'''
    if not hasattr(data, '__iter__'):
        raise TypeError('data must be an iterable')
    if any(not isinstance(item, int) for item in data):
        raise TypeError('radix sort only works with integers')
    if len(data) == 0:
        return data.copy()
    if any(item < 0 for item in data):
        raise ValueError('all items must be positive')

    result = data.copy()
    if isinstance(result, ndarray):
        result = result.tolist()
 #Find the maximum number to determine the number of digits
    max_num = max(result)
    num_digits = 1
    while max_num // base > 0:
        max_num //= base
        num_digits += 1

    #Iterate through each digit position
    for digit_place in range(num_digits):
        # Create buckets for each possible digit
        buckets = [[] for _ in range(base)]

        #Distribute elements into buckets based on the current digit
        for num in result:
            digit = (num // base**digit_place) % base
            buckets[digit].append(num)

        # Concatenate buckets back into the result
        result = [num for bucket in buckets for num in bucket]

    return result

#___Search Algorithms___
def linearsearch(data, target):
    '''Search for a target value in a list using a linear approach.
    \nTime Complexity: O(n)'''
    if not hasattr(data, '__iter__'):
        raise TypeError('data must be an iterable')
    datalist = data.copy()
    if isinstance(data, ndarray):
        datalist = datalist.tolist()

    for i in range(len(datalist)):
        if datalist[i] == target:
            return i
    return -1   

def binarysearch(data, target):
    '''Perform a binary search on a sorted list.
    \nTime Complexity: O(log n)
    \nPrecondition: the list is sorted.'''
    if not hasattr(data, '__iter__'):
        raise TypeError('data must be an iterable')
    datalist = data.copy()
    if isinstance(datalist, ndarray):
        datalist = datalist.tolist()
    if not isinstance(datalist, list):
        new_datalist = []
        for i in datalist:
            new_datalist.append(i)
        datalist = new_datalist
    if datalist != sorted(datalist):
        raise ValueError('data must be sorted')

    low = 0
    high = len(data) - 1

    while low <= high:
        mid = (low + high) // 2
        if datalist[mid] == target:
            return mid
        elif datalist[mid] < target:
            low = mid + 1
        else:
            high = mid - 1

    return -1

def interpolationsearch(data, target):
    '''Perform an interpolation search on a sorted list.
    \nTime Complexity: O(log(log n)) (best case), O(n) (worst case)
    \nPrecondition: the list is sorted.'''
    if not hasattr(data, '__iter__'):
        raise TypeError('data must be an iterable')
    datalist = data.copy()
    if isinstance(datalist, ndarray):
        datalist = datalist.tolist()
    if datalist != sorted(datalist):
        raise ValueError('data must be sorted')

    low = 0
    high = len(datalist) - 1

    while low <= high and target >= datalist[low] and target <= datalist[high]:
        # Estimate the position using interpolation formula
        pos = low + ((high - low) * (target - datalist[low]) // (datalist[high] - datalist[low]))

        if datalist[pos] == target:
            return pos
        elif datalist[pos] < target:
            low = pos + 1
        else:
            high = pos - 1

    return -1