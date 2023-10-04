CS685 - Internet Data Streaming 
Project 2 - Implementation of Bloom Filters
Author: Bobby Bose

Description
- This is an implementation of three types of bloom filters: regular bloom filters, counting bloom filters, and coded bloom filters
- There are three Python scripts, one for each bloom filter implementation
- An example output is given in three output (.out) files
- Hash function used in all code was based off of the folding method from https://www.herevego.com/hashing-python/

Required Packages and Modules
- No external packages required 
- The only required modules are the sys, random, and math modules built into Python

Bloom Filter
- To run, do 'python ./bloom_filter.py num_elements_to_encode num_bits_in_filter num_hashes'
- Architecture Operation:
    - Encodes a given number of elements into a standard bloom filter
        - Bloom filter is a bitmap initially filled with 0's
    - Each element is hashed to a given number of bits in the filter and encoded to each one
        - Each hashed entry is set to be 1, to indicate that the entry is encoded
- Program Flow: 
    - Generates a given number of random elements (set A)
    - Encodes set A into the filter
    - Lookup how many elements of set A are found in the filter
    - Generates another given number of random elements (set B)
    - Lookup how many elements of set B are falsely found to be in the filter
- Output
    - First line is number of elements of set A found in the filter after encoding
    - Second line is number of elements of set B found in the filter without encoding (false positives)

Counting Bloom Filter
- To run, do 'python ./counting_bloom_filter.py num_elements_to_encode num_elements_to_remove num_elements_to_add num_counters_in_filter num_hashes'
- Architecture Operation:
    - Encodes a given number of elements into a counting bloom filter
        - Counting bloom filter is an array/list of counters
    - Each element is hashed to a given number of counters in the filter and encoded to each one
        - Each hashed entry counter is incremented by 1, to indicate that the entry is encoded
    - Elements are also able to be removed from the filter
        - When removing an element, each counter the element is hashed to decrements its count be 1
- Program Flow: 
    - Generates a given number of random elements (set A)
    - Encodes set A into the filter
    - Remove a given number of elements from the filter
    - Add another given amount of elements into the filter
    - Lookup how many of the original elements from set A are found in the filter
- Output
    - How many elements from set A were found during lookup

Coded Bloom Filter
- To run, do 'python ./coded_bloom_filter.py num_sets num_elements_per_set num_filters num_bits_per_filter num_hashes'
- Architecture Operation:
    - Encodes a given number of sets of elements to a given number of standard bloom filters
        - The number of elements in each set is given
        - The number of bits in each filter is given
    - Each set has a unique set code of length ceiling(log_2(num_sets+1)) bits
        - For demo example of 7 sets, the code is 3 bits long
        - Each bit of the set code represents a different bloom filter
        - If the bit is 1, then all elements from the set should be encoded in the corresponding bloom filter
    - When encoding an element in a filter, the element is hashed to a given number of bits
- Program Flow: 
    - Generates a given number of sets of a given number of elements each
        - Assign a unique set code to each set
    - Encode all sets in the given number of bloom filters according to the algorithm explained above
    - Lookup all elements in all sets
- Output
    - How many elements had correct lookup results
