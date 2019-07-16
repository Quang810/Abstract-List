import timeit
class HashTable():
    def __init__(self, table_capacity = 31, hash_base=1):
        """
        Pre-condition: None
        Post_condition: An array with the size of table_capacity. If table_capacity is not defined, default value
        which is 31 will be used
        Big-O complexity: O(1)
        :param table_capacity: default value at 31
        :param hash_base: default value at 101
        """
        self.count = 0 #The number of item in the hash table
        self.capacity = table_capacity
        self.base = hash_base
        self.array = [None] * self.capacity
        self.skip = 1 #skip k using for hash function

        self.rehash_count = 0
        self.probe_total = 0
        self.probe_max = 0
        self.collision_count = 0

    def hash(self, key):
        """
        Pre-condition: A none empty array
        Post-condition: position of each key
        Big-O complexity O(1)
        :param key: hash key
        :return: position of each hash key
        """
        h = 0
        a = self.base
        for i in range(len(key)):
            h = (h * a + ord(key[i])) % self.capacity
        return h

    def __str__(self):
        """
        translate each element inside hash table into string
        Pre-condition: Hash table with element not None
        Post-condition: Hash value with each element in string type
        Big-O complexity: O(n) which n is the length of the array
        :return: hash table with each element in string type
        """
        table = "Hashtable of size" + str(self.count) + \
            " and capacity " + str(self.capacity) + "\n"

        for i, tuple in enumerate(self.array):
            table += str(i) + "," + str(tuple) + "\n"
        return table

    def isfull(self):
        return self.count == len(self.array)

    def __setitem__(self, key, value):
        """
        set element at key position equal to value
        Pre-condition: None empty hash table
        Post-condition: Hash table in which value at key position
        Big-O complexity: O(n) which n is the length of the array
        :param key: hash key
        :param value: value at hash key position
        :return: hash table in which value at key position
        """
        position = self.hash(key)
        original_pos = position
        probe_length = 0
        flag = False
        check_collision = False
        step = 0
        while not flag:
            if self.array[position] is None:
                if probe_length >= self.probe_max:
                    self.probe_max = probe_length
                self.array[position] = (key, value)
                self.probe_total += probe_length
                self.count += 1
                flag = True
            elif self.array[position][0] == key:
                self.array[position] = (key, value)
                flag = True
            else:
                if not check_collision:
                    check_collision = True
                    self.collision_count += 1
                probe_length += 1
                #step += 1
                position = (original_pos + self.skip**2) % self.capacity
                self.skip += 1

        if self.isfull():
            self.rehash()
            self.__setitem__(key, value)


    def __getitem__(self, key):
        """
        return the value at key position
        Pre-condition: Hash table with value at key position
        Post-condition: value at key position
        Big-O complexity: O(n) with n the the length of the array
        :param key: hash key
        :return: value at key position
        """
        position = self.hash(key)
        original_pos = position
        step = 0
        for _ in range (self.capacity):
            if self.array[position] is None:
                raise KeyError(key)
            elif self.array[position][0] == key:
                return self.array[position][1]
            else:
                #step += 1
                position = (original_pos + (self.skip**2))%self.capacity
                self.skip += 1
        raise KeyError(key)

    def __contains__(self, key):
        """
        Check whether there is key in the table
        Pre-condition: None empty hash table
        Post-condition: True if there is such key in the table, False if otherwise
        Big-O complexity: O(n) with n is the length of the array
        :param key: hash key
        :return: True or False
        """
        if self.count >= self.capacity:
            raise IndexError ("The array is full")
        flag = False
        position = self.hash(key)
        try:
            while not flag:
                if self.array[position][0] == key:
                    flag = True
                    return True
                else:
                    if self.array[position] is None:
                        position = (position + self.skip) % self.capacity
            return False
        except:
            return False

    def rehash(self):
        """
        creates a new array using as size the smallest prime number in the Primes
        list below that is larger than twice the current size. It then updates the size of the hash table
        and reinserts all key-value pairs in the old array into the new array using the new size
        Pre-condition: Full hash table
        Post-condition: New hash table in which size is the prime number which is larger than double previous size.
        The new hash table contains all the element of the old table
        Big-O complexity:
        Need fix. loop through the list, if i > new capacity, then assign that to new capacity
        :return:
        """

        self.rehash_count += 1
        primes = [3, 7, 11, 17, 23, 29, 37, 47, 59, 71, 89, 107, 131, 163, 197, 239, 293, 353, 431, 521, 631, 761,
                  919, 1103, 1327, 1597, 1931, 2333, 2801, 3371, 4049, 4861, 5839, 7013, 8419, 10103, 12143, 14591,
                  17519, 21023, 25229, 30293, 36353, 43627, 52361, 62851, 75431, 90523, 108631, 130363, 156437,
                  187751, 225307, 270371, 324449, 389357, 467237, 560689, 672827, 807403, 968897, 1162687, 1395263,
                  1674319, 2009191, 2411033, 2893249, 3471899, 4166287, 4999559, 5999471, 7199369]

        temp_list = self.array
        find_prime = False

        double_size = self.capacity * 2
        for number in primes:
            if number > double_size:
                self.capacity = number
                find_prime = True
                break
        if not find_prime:
            raise ValueError("There is no such prime in the list")

        self.array = [None] * self.capacity
        self.count = 0
        for i in range(len(temp_list)):
            if temp_list[i] is not None:
                self.__setitem__(temp_list[i][0], temp_list[i][1])

    def statistics(self):
        """
        Pre-condition: None empty hash table
        Post-condition: list which contains numbers of collisions, total length of probe chain, longest probe length
        Big-O complexity: O(1)
        :return:a list which contains numbers of collisions, total length of probe chain, longest probe length
        and total time rehash function is called
        Need fix: just count for the probe, collision count is the probe length, probe_total adding after each turn, probe_max first initial is 0. Then compare the later with the first. If the later is bigger, new max
        """
        Statistic = (self.collision_count, self.probe_total, self.probe_max, self.rehash_count)

        return Statistic

def load_dictionary(hashtable, filename):
    '''
    Read the data from the file and place it into the table
    Pre-condtion: None
    Post-condition: Hash table with data read from the file
    Big-O complexity: O(n) which n is the length of the data
    :param hashtable: new hashtable
    :param filename: Name of the file which needed to read the data
    :return: None
    '''
    file = open(filename, 'r')
    start = timeit.default_timer()
    try:
        for line in file:
            temp = line.strip("\r\n")
            hashtable[temp] = 1
            statistics = hashtable.statistics()
            stop = timeit.default_timer() - start
            if (stop > 3):
                raise Exception
    except Exception:
        stop = "Time out"
    file.close()
    return (stop, statistics[0], statistics[1], statistics[2], statistics[3])



def main():
    '''
                                           Filename                                      Hashtable size                                      Hashtable base                                        Running time                                 Number of collision                                   Total probe chain                                 Maximum probe chain                               Number of rehash time
                                 english_small.txt                                              250727                                                   1                                      0.920762062073                                               82626                                              100789                                                  10                                                   0
                                 english_large.txt                                              250727                                                   1                                       1.38002681732                                              192845                                              373152                                                  77                                                   0
                                        french.txt                                              250727                                                   1                                       1.58224391937                                              200503                                              411425                                                  78                                                   0
                                 english_small.txt                                              402221                                                   1                                      0.505140066147                                               82608                                               92712                                                   7                                                   0
                                 english_large.txt                                              402221                                                   1                                        1.2514359951                                              192765                                              264267                                                  13                                                   0
                                        french.txt                                              402221                                                   1                                       1.51516389847                                              200418                                              279294                                                  15                                                   0
                                 english_small.txt                                             1000081                                                   1                                      0.674201011658                                               82565                                               86240                                                   4                                                   0
                                 english_large.txt                                             1000081                                                   1                                       1.26236605644                                              192713                                              214480                                                   6                                                   0
                                        french.txt                                             1000081                                                   1                                       1.34623003006                                              200315                                              224309                                                   8                                                   0
                                 english_small.txt                                              250727                                               27183                                       0.52586889267                                               14057                                               18276                                                   7                                                   0
                                 english_large.txt                                              250727                                               27183                                       1.27110099792                                               75483                                              180830                                                  40                                                   0
                                        french.txt                                              250727                                               27183                                       1.40939211845                                               81975                                              210103                                                  45                                                   0
                                 english_small.txt                                              402221                                               27183                                      0.476016998291                                                8808                                               10224                                                   6                                                   0
                                 english_large.txt                                              402221                                               27183                                       1.25890278816                                               47193                                               71327                                                  13                                                   0
                                        french.txt                                              402221                                               27183                                       1.47611713409                                               50751                                               78990                                                  16                                                   0
                                 english_small.txt                                             1000081                                               27183                                      0.637562990189                                                3424                                                3627                                                   4                                                   0
                                 english_large.txt                                             1000081                                               27183                                        1.1868481636                                               18671                                               21564                                                   5                                                   0
                                        french.txt                                             1000081                                               27183                                       1.19612979889                                               20451                                               23568                                                   6                                                   0
                                 english_small.txt                                              250727                                              250726                                      0.641505002975                                               83839                                              102225                                                  10                                                   0
                                 english_large.txt                                              250727                                              250726                                       1.35125899315                                              194177                                              375527                                                  37                                                   0
                                        french.txt                                              250727                                              250726                                       1.72474002838                                              201862                                              413487                                                  43                                                   0
                                 english_small.txt                                              402221                                              250726                                      0.505588054657                                                8810                                               10277                                                   6                                                   0
                                 english_large.txt                                              402221                                              250726                                       1.18357801437                                               46992                                               71505                                                  11                                                   0
                                        french.txt                                              402221                                              250726                                       1.38112783432                                               50732                                               78683                                                  14                                                   0
                                 english_small.txt                                             1000081                                              250726                                      0.488775968552                                                3506                                                3735                                                   3                                                   0
                                 english_large.txt                                             1000081                                              250726                                       1.28058481216                                               18732                                               21609                                                   5                                                   0
                                        french.txt                                             1000081                                              250726                                       1.23040890694                                               20584                                               23863                                                   6                                                   0

        The quadratic probing is a big improvement compared to linear probing. No more time out for all the combination
        This happens because the clustering growth is much slower now. The linear probing change the position when it spot at that position, a key is already existed.
        However, the linear probing with the function position = (position + self.skip) / table_capacity only move by one index everytime a collision happens
        The quadratic probing moves by i**2 (We look for i**2th slot in the i iteration) index everytime a collision happens. This method moves the index exponential, slowing down the clustering process
        Comparing the data from quadratic probing with linear probing, the maximum probe chain drops significantly. This is why everytime collision happens,
        the index jump exponentially
        The total probe chain also drops significantly. Again, The quadratic probing moves by i**2 index after ith iteration.
        The increasing of collision count is expected. This is because the index jump i**2 after ith iteration
        Jumping index exponentially increases the chance of meeting the position which key is already occupied.
        The size of the table is reasonably large, so no rehash happens
    :return:
    '''
    print ('{:>50}  {:>50}  {:>50}  {:>50}  {:>50}  {:>50}  {:>50}  {:>50}'.format('Filename', 'Hashtable size', 'Hashtable base', 'Running time', 'Number of collision', 'Total probe chain', 'Maximum probe chain', 'Number of rehash time' ))
    for b in [1, 27183, 250726]:
        for size in [250727, 402221, 1000081]:
            for book in ['english_small.txt', 'english_large.txt', 'french.txt']:
                Result = load_dictionary(HashTable(size, b), book)
                print('{:>50}  {:>50}  {:>50}  {:>50}  {:>50}  {:>50}  {:>50}  {:>50}'.format(book, size, b, Result[0], Result[1], Result[2], Result[3], Result[4]))


main()




