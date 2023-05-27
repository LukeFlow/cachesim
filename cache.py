import argparse
import random

# CacheBlock class represents a single cache block
class CacheBlock:
    def __init__(self, tag, data, valid=False, dirty=False):
        self.tag = tag
        self.data = data
        self.valid = valid
        self.dirty = dirty


# CacheSet class represents a set of cache blocks
class CacheSet:
    def __init__(self, set_size, block_size, replacement_policy):
        self.set_size = set_size
        self.block_size = block_size
        self.replacement_policy = replacement_policy
        self.blocks = [None] * set_size
        if replacement_policy == "FIFO":
            self.replacement_queue = list(range(set_size))
        elif replacement_policy == "LRU":
            self.replacement_queue = []
        elif replacement_policy == "Random":
            self.replacement_queue = []

    # Check if a block with the given tag is present in the set
    def contains(self, tag):
        for block in self.blocks:
            if block is not None and block.tag == tag:
                return True
        return False

    # Find a free block in the set, or the block to replace based on the replacement policy
    def find_victim(self):
        for i in range(self.set_size):
            if self.blocks[i] is None:
                return i
        if self.replacement_policy == "FIFO":
            victim_index = self.replacement_queue.pop(0)
            self.replacement_queue.append(victim_index)
            return victim_index
        elif self.replacement_policy == "LRU":
            victim_index = self.replacement_queue.pop(0)
            self.replacement_queue.append(victim_index)
            return victim_index
        elif self.replacement_policy == "Random":
            victim_index = random.randint(0, self.set_size - 1)
            return victim_index

    # Replace the block at the given index with a new block with the given tag and data
    def replace_block(self, index, tag, data, dirty=False):
        self.blocks[index] = CacheBlock(tag, data, True, dirty)
        if self.replacement_policy == "LRU":
            self.replacement_queue.remove(index)
            self.replacement_queue.append(index)

    # Write data to a block with the given tag
    def write_data(self, tag, data):
        for block in self.blocks:
            if block is not None and block.tag == tag:
                block.data = data
                block.dirty = True
                break

    # Read data from a block with the given tag, returns None if the block is not present
    def read_data(self, tag):
        for block in self.blocks:
            if block is not None and block.tag == tag:
                return block.data
        return None

    # Return the tag of the block at the given index
    def get_tag(self, index):
        if self.blocks[index] is not None:
            return self.blocks[index].tag
        else:
            return None


# Cache class represents a cache with multiple sets
class Cache:
    def __init__(self, num_sets, set_size, block_size, replacement_policy, write_policy):
        self.num_sets = num_sets
        self.set_size = set_size
        self.block_size = block_size
        self.replacement_policy = replacement_policy
        self.write_policy = write_policy
        self.sets = [CacheSet(set_size, block_size, replacement_policy) for i in range(num)]
