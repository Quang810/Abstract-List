from math import floor, ceil


class ListADT:

    def __init__(self, size=35):
        if size < 0:
            raise Exception("Size must be greater than 0")
        self.the_array = [""] * size
        self.array_size = size
        self.length = 0
        self.in_test_mode = True

    def __str__(self):
        """
        return a list, each element is a string of previous list
        Pre-condition: None
        Post-condition: list of string
        Big-O complexity: O(n) with n is the length of the array
        :return:
        """
        string = ""
        if not self.is_empty():
            for index in range(self.length):
                string += str(self.the_array[index])
                string += "\n"
        return string

    def __len__(self):
        """
        return length of the array
        Pre-condition: None
        Post_condition: length of the array
        Big-O complexity: O(1)
        :return:
        """
        return self.length

    def __getitem__(self, index):
        """
        return the item at the_array[index] position
        Pre-condition: the_array
        Post-condition: item at the_array[index] position
        Raise Value Error if the array is empty
        :param index: index of the array in which user want to retrieve the item
        Big-O complexity: O(1)
        :return:
        """
        if not self.is_empty():
            return (self.the_array[index])
        else:
            raise ValueError

    def __setitem__(self, index, item):
        """
        set the_array[index] to be equal to item
        Pre_condition: The array
        Post_condition: The array in which the value at index position is equal to item
        Raise ValueError if index is larger than size of index
        :param index: index of the array
        :param item: value that user want to switch to the value of the array at index position
        :return:
        """
        if not self.is_empty():
            if index < self.array_size:
                self.the_array[index] = item
        else:
            raise IndexError("Index out of range")

    def __eq__(self, other):
        """
        compare length of the array with length of the other array. If it is not equal, return false immediately. Then compare if whether each value of the array is equal to matched value of the other array
        pre-condition: the _array
        post-condition: True if the array is equal to the other array, False if two array does not match
        Big-O complexity:
        Best case: O(1) if the lengths of two array does not match
        Worst case: O(n) with n is the length of the array
        :param other: other array
        :return: True, or False
        """
        if (len(self) != len(other)):
            return False

        for i in range(len(self)):
            if self.the_array[i] != other.the_array[i]:
                return False
        return True


    def insert(self, index, item):
        """
        Inserts item into self at position index
        Pre-condition: the array
        Post-condition: the array in which value at index position is equal to item
        Raise IndexError if the index is out of size range
        Big-O complexity:
        Best case: O(1) if the index is out of range
        Worst case: O(n) with n is the length of the array
        :param index:
        :param item:
        :return: the new array
        """
        if index >= self.array_size:
            raise IndexError("Index out of range")

        else:
            if index<0:
                index=self.length+index
            for i in range(self.length, index, -1):
                self.the_array[i] = self.the_array[i-1]

        self.the_array[index]=item
        self.length+=1
        self.resize()

    def delete(self, index):
        """
          Delete the item at index position
        Pre-condition: the array
        Post-condition: shorten array
        Big-O complexity: O(n) for n is the length of the array
        :param index: index position of the array
        :return: new shorten array
        """
        returnValue = self.the_array[index]
        if index not in range(self.length):
            raise IndexError("Index is out of range")
        elif self.is_empty():
            raise Exception("The array is empty")
        else:
            for i in range (index, self.length):
                self.the_array[i] = self.the_array[i+1]

        self.the_array[len(self) - 1] = None
        self.length -= 1
        self.resize()

        return(returnValue)
    # def __setitem__(self, index, item):

    def is_empty(self):
        """
               return whether array is empty or not (True or False)
               Pre-condition: an array
               Post-condition: True or False
               Big-O complexity: O(1)
               :return: length of the array is whether 0 or not
               """
        return self.length == 0

    def is_full(self):
        """
                return whether array is full or not (True of False)
                Pre-condition: an array
                Post-condition: True or False
                Big-O complexity: O(1)
                :return: the array is full or not (True or False)
                """
        return self.length == len(self.the_array)

    def __contains__(self, item):
        """
                return whether the array contain the item or not (True or False)
                Pre-condition: an not empty array
                Post-condition: True if the item in the array. False if the item is not in the array
                Big-O complexity: O(n) in which n is the length of the array
                :param item: item that user want to check
                :return: True or False
                """
        for i in range(self.length):
            if item == self.the_array[i]:
                return True
        return False

    def append(self, item):
        """
                append item in the array if the array is not full
                Pre-condition: Not full array
                Post-condition: item inserted into the array
                Big-O complexity: O(1)
                :param item: item that user want to input
                :return: None
                """
        if not self.is_full():
            self.the_array[self.length] = item
            self.length += 1
            self.resize()
        else:
            raise Exception('List is full')


    def resize(self):
        """
        Resize array to new array
        Pre-condition: A not empty array must exist
        Post-condition: Bigger or smaller array, depends on the length of the array
        Big-O complexity: O(n) with n is the length of the array
        Raise Exception if the list is empty
        """


        if self.is_empty():
            raise Exception('The array is empty')

        if self.is_full():
            self.array_size = ceil(self.array_size * 1.6)
            self.array_size = int(self.array_size)

        if self.length <=self.array_size/4:
            self.array_size = self.array_size/2
        Aux_Array=[""]*self.array_size
        for i in range(self.length):
            Aux_Array[i]=self.the_array[i]
        self.the_array=Aux_Array



    def unsafe_set_array(self, array, length):
        """
        use to test above functions
        Pre-condition: Non empty list
        Post-condition: A tested array
        Big-O complexity: O(1)
        UNSAFE: only to be used during testing to facilitate it!! DO NOT USE FOR ANYTHING ELSE
        """
        try:
            assert self.in_test_mode
        except:
            raise Exception('Cannot run unsafe_set_array outside testing mode')

        self.the_array = array
        self.length = length
