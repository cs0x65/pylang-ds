"""
The objective here is not to implement a substitute for the in-built `dict`. The focus is on how - for a given key,
we can map it to a unique numeric value. This is important because, the very premise underlying the hash table is that
we can use the prevailing numeric value as an index into an array where the given key-value pair shall be stored.

It's essential to note that for Python or for that matter any programming language, the hash table implementation needs
to map any given key to a unique number which shall act as an index into **a finite array within the memory bounds.**
Which means, a numeric hash function like (or their variations) - FNV, MurmurHash, CityHash, SipHash etc. is used
internally; typically these functions will produce a large number which is again mapped to a smaller number using the
modulo operator such that it resolves to an index into finite array of buckets in RAM.

References:
    - https://benhoyt.com/writings/hash-table-in-c/
    - https://craftinginterpreters.com/hash-tables.html
    - https://en.wikipedia.org/wiki/Non-cryptographic_hash_function

Typical implementation looks like below:
::

    effective_hash = non_cryptographic_fn_like_fnv_murmur_siphash(key) % num_buckets

For any programming language, in general, string is a reliable & obvious choice for a key as the language will use one
of the above-mentioned numeric hash functions to generate a unique number for the string. Even for user defined classes
that implement their own hashing logic by overriding __hash__() in Python or hashCode() in Java, it's still preferable
to leverage the string field(s) of the class to generate a unique number.

::

    # python
    >>> s = 'hello pyshell'
    >>> s.__hash__()
    >>> -4446671785528942560

    # java
    jshell> String s = "hello jshell";
    s ==> "hello jshell"

    jshell> System.out.println(s.hashCode());
    -586076396
"""
from typing import Any


class PycsDictEntry:
    """
    A class representing an entry in the hash table.
    """
    def __init__(self, key: str, value: Any):
        self.key = key
        self.value = value
        # With this, a support is in place for a possible linked list construction for handling collisions.
        # It's upto the implementation of the `PycsDict` class to decide how to handle the collisions - linked list,
        # sequential list or trees.
        self.next_entry = None

    def __str__(self):
        return f'{self.key}: {self.value}'


class PycsDict:
    FNV1A_OFFSET: int = 14695981039346656037
    FNV1A_PRIME: int = 1099511628211
    LOAD_FACTOR: float = 0.75

    def __init__(self, size: int):
        self.size = size or 8
        # Allocate the initial capacity to twice the size to reduce collisions
        self.capacity = size * 2

        self.table: Any = [None] * self.capacity
        """
        This will actually allocate the list with given capacity i.e. it will create a list of given capacity where
        all the list elements are `None` values. This is different from:
        
        :: 
            
            self.table = []
            # or
            self.table = list()
        When it's an empty list, we keep on appending the elements - self.table.append(PycsDictEntry(key, value)).
        But when we allocate the list with a given capacity, we can directly access index in the list & also set the 
        value at that index - self.table[bucket_index] = PycsDictEntry(key, value).
        This is was the root cause why the `KeyError` was being raised when trying to access the key earlier -- 
        because the code was inserting the entry/bucket at the given index 
        self.table.insert(bucket_index, PycsDictEntry(key, value)) rather than setting the entry/bucket at the index 
        self.table[bucket_index] = PycsDictEntry(key, value). The insertion used to change the list size and hence, 
        _get_bucket_index function was returning a different index than the one where the entry was actually stored.
        """

    @staticmethod
    def _get_hash(key: str) -> int:
        """
        Hashing function to convert a string key into a numeric value.
        """
        hash_value = PycsDict.FNV1A_OFFSET
        for char in key:
            hash_value ^= ord(char)
            hash_value *= PycsDict.FNV1A_PRIME
        return hash_value

    @staticmethod
    def _get_bucket_index(hash_value: int, capacity: int) -> int:
        """
        Get the bucket index for a given hash value.
        """
        return hash_value % capacity

    def __getitem__(self, key: str) -> Any:
        bucket_index =  PycsDict._get_bucket_index(PycsDict._get_hash(key), self.capacity)
        entry = self.table[bucket_index]
        if isinstance(entry, PycsDictEntry):
            if entry.key == key:
                return entry.value
        elif isinstance(entry, list):
            bucket = entry
            for e in bucket:
                if e.key == key:
                    return e.value
        raise KeyError(f'{self.__class__.__name__} Key {key} not found in dictionary.')

    def __setitem__(self, key: str, value: Any):
        # TODO: add support for resizing the table when load factor exceeds threshold
        bucket_index = PycsDict._get_bucket_index(PycsDict._get_hash(key), self.capacity)
        entry = self.table[bucket_index]
        old_value = value
        if entry is None:
            self.table[bucket_index] = PycsDictEntry(key, value)
        elif isinstance(entry, PycsDictEntry):
            if entry.key == key:
                old_value = entry.value
                entry.value = value
            else:
                # Collision resolution using sequential list - a bucket is created to hold the multiple entries being
                # hashed to this index; the implementation can be replaced with a linked list, if required
                bucket: Any = [None] * int(self.capacity / 4)
                bucket.append(entry)
                bucket.append(PycsDictEntry(key, value))
                self.table[bucket_index] = bucket
        else:
            # Collision - search sequentially in the bucket
            bucket = entry
            for e in bucket:
                if e.key == key:
                    old_value = e.value
                    e.value = value
                    break
            # If the key was not found in the bucket, append a new entry
            bucket.append(PycsDictEntry(key, value))
        return old_value

    def __str__(self):
        """
        String representation of the PycsDict.
        """
        entries = []
        for entry in self.table:
            if isinstance(entry, PycsDictEntry):
                entries.append(str(entry))
            elif isinstance(entry, list):
                for e in entry:
                    entries.append(str(e))
        return '{' + ', '.join(entries) + '}'


if __name__ == '__main__':
    # Example usage
    pycs_dict = PycsDict(10)
    pycs_dict['email'] = 'saurabh.cse2@gmail.com'
    pycs_dict['city'] = 'Pandharpur'
    pycs_dict['passion'] = 'Computer Science, Software Engineering & Technology'

    print(f'pycs_dict = {pycs_dict}')

    print(f'Hi there! I am {pycs_dict["email"]} from {pycs_dict["city"]} and am passionate about'
          f' {pycs_dict["passion"]}.')
    pycs_dict['city'] = 'Bengaluru'
    print(f'I am currently located in {pycs_dict["city"]}.')
    print(pycs_dict['dob'])

