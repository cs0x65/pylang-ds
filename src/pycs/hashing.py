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

class PycsDict:
    pass