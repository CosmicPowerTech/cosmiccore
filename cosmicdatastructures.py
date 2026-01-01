'''Cosmic Core: Cosmic Data Structures
\n\tA library of basic data structures, including stacks, queues, lists, and trees.'''
from numpy import array, ndarray
from .cosmicalgorithms import *
__all__ = ['node', 'dlnode', 'tnode', 'pnode', 'chain', 'dlchain', 'bag',
           'stack', 'queue', 'priorityqueue', 'linklist', 'dlinklist', 'tree']

#___Linked Chain Basics___
#Used to construct link-based data structures.
class node(object):
    '''Represents a singly linked node.'''

    def __init__(self, data, next = None):
        self.data = data
        self.next = next

class dlnode(node):
    '''Represents a doubly linked node.'''

    def __init__(self, data, next = None, prev = None):
        super().__init__(data, next)
        self.prev = prev

class pnode(node):
    '''Represents a singly linked node with a priority assigned to it.'''

    def __init__(self, data, next = None, priority = 0):
        super().__init__(data, next)
        if not isinstance(priority, int):
            raise TypeError('priority must be an int')
        self.priority = priority

class tnode(object):
    '''Represents a node in a general tree.'''
    def __init__(self, data, children = None, max_children = None, parent = None):
        self.data = data
        if not isinstance(max_children, int) and max_children is not None:
            raise TypeError('max_children must be an int')
        if children is None:
            children = []
        if not isinstance(children, (list, linklist, dlinklist, ndarray)):
            raise TypeError('children must be a list, linked list, or NumPy array')
        if isinstance(children, ndarray):
            children = children.tolist()
        self.children = children
        self.max_children = max_children
        self.parent = parent

    def isleaf(self):
        '''Return True if the node has no children, False otherwise.'''
        return len(self.children) == 0
    
    def add(self, item):
        '''Add new child to the node.'''
        if self.max_children is not None and len(self.children) >= self.max_children:
            raise ValueError('maximum number of children per node reached')
        self.children.append(tnode(item, [], self.max_children, self))
    
    def pop(self, i):
        '''Remove and return the child at position i.'''
        if self.isleaf():
            raise ValueError('cannot pop from a leaf')
        try:
            child = self.children.pop(i)
            child.parent = None  # Remove parent reference
            return child
        except IndexError as e:
            raise e
        
    def remove(self, item):
        '''Remove the first instance of item in the children list.'''
        if self.isleaf():
            raise ValueError('cannot remove from a leaf')   
        
        for i in range(len(self.children) -1, -1, -1):
            if self.children[i].data == item:
                child = self.children.pop(i)
                child.parent = None  # Remove parent reference
                return
            
        raise ValueError(f'{item} is not a child of this node')
    
    def depth(self):
        '''Return the depth of the node (distance from the root).'''
        depth = 0
        current = self
        while current.parent is not None:
            current = current.parent
            depth += 1
        return depth

    def __getitem__(self, i):
        '''Return the item at position i.'''
        return self.children[i]
    
    def __str__(self):
        '''Return the string representation of the node.'''
        if self.isleaf():
            return f'{self.data}'
        else:
            children_str = '['
            for i in self.children:
                children_str += str(i) + ', '
            children_str = children_str[:-2]
            children_str += ']'
            return f'{self.data}: {children_str}'

class chain(object):
    '''A template for linked chain-based data structures.'''

    def __init__(self, source_collection = None):
        '''Set the initial state of self, which includes the
        contents of sourceCollection, if it's present.'''

        self.head = self.tail = None
        self.size = 0
        
        if source_collection is not None:
            for i in source_collection:
                self.add(i)

    def add(self, item):
        '''Add item to self.'''
        #This function will have varying definitions based on the data type,
        #but the base definition will be what is used with queues and lists.
        new_node = node(item)

        if self.size == 0:
            self.head = new_node
        else:
            self.tail.next = new_node
        
        self.tail = new_node
        self.size += 1

    def clear(self):
        '''Make self become empty.'''
        
        self.head = self.tail = None
        self.size = 0

    def copy(self):
        '''Return a copy of self.'''
        copy_chain = type(self)()
        copy_chain.extend(self)
        return copy_chain
    
    def extend(self, other):
        '''Add the contents of other to self.'''
        for i in other:
            self.add(i)

    def isempty(self):
        '''Return True if len(self) == 0, or False otherwise.'''
            
        return self.size == 0
    
    def __add__(self, other):
        '''Return a new instance of the type of self
        containing the contents of self and other.'''
        
        new_chain = type(self)(self)
        if isinstance(other, (list, tuple, set, chain)):
            new_chain.extend(other)
        else:
            new_chain.add(other)
        return new_chain
    
    def __contains__(self, item):
        '''Return True if self contains the item, False otherwise.'''
        cur_node = self.head
        while cur_node != None:
            if cur_node.data == item:
                return True
            cur_node = cur_node.next
        return False
    
    def __eq__(self, other):
        '''Return True if self equals other, or False otherwise.'''
        
        if self is other:
            return True
        
        if type(self) != type(other):
            return False
        
        if len(self) != len(other):
            return False
        
        cur_self_node = self.head
        cur_other_node = other.head
        while cur_self_node != None and cur_other_node != None:
            if cur_self_node.data != cur_other_node.data:
                return False
            cur_self_node = cur_self_node.next
            cur_other_node = cur_other_node.next

        return True
    
    def __iter__(self):
        '''Iterate over a view of self.'''
        
        cursor = self.head
        while cursor != None:
            yield cursor.data
            cursor = cursor.next
        
    def __len__(self):
        '''Return the number of items in self.'''
        
        return self.size
    
    def __str__(self):
        '''Return the string representation of self.'''
        chain_string = ''
        
        cur_node = self.head
        while cur_node != None:
            chain_string += str(cur_node.data) + ', '
            cur_node = cur_node.next
                    
        chain_string = f'{{{chain_string[:-2]}}}'
        
        return chain_string
    
    def __repr__(self):
        return f'chain({str(self)})'
        
class dlchain(chain):
    '''A template for doubly linked chain-based data structures.'''

    def add(self, item):
        '''Add item to self.'''
        #This function will have varying definitions based on the data type,
        #but the base definition will be what is used with queues and lists.
        new_node = dlnode(item)

        if self.size == 0:
            self.head = new_node
        else:
            self.tail.next = new_node
        
        new_node.prev = self.tail
        self.tail = new_node
        self.size += 1    

#___Basic Data Structures___
class bag(chain):
    '''A link based bag (multiset) implementation.'''
    def add(self, item):
        '''Add item to the bag.'''
        new_node = node(item)
        new_node.next = self.head
        self.head = new_node
        self.size += 1

    def count(self, item):
        '''Return the number of instances of the item in the bag.'''
        count = 0
        cur_node = self.head
        while cur_node != None:
            if cur_node.data == item:
                count += 1
            cur_node = cur_node.next
        return count

    def remove(self, item):
        '''Remove an item from the bag.'''
        cur_node = self.head
        while cur_node != None:
            if cur_node.data == item:
                break
            cur_node = cur_node.next
        if cur_node == None:
            raise KeyError(f'{item} is not in the bag')
        
        # swap data to remove with head node data
        cur_node.data, self.head.data = self.head.data, cur_node.data

        # make the 2nd node to the new head node
        self.head = self.head.next

        self.size -= 1

    def __eq__(self, other):
        '''Return True if self equals other, or False otherwise.'''

        if self is other:
            return True
        
        if type(self) != type(other):
            return False
        
        if len(self) != len(other):
            return False

        for i in self:
            if self.count(i) != other.count(i):
                return False
            
        return True

class stack(chain):
    '''A link-based stack implementation.'''
    def __init__(self, source_collection = None):
        '''Set the initial state of self, which includes the
        contents of sourceCollection, if it's present.'''

        self.head = self.tail = None
        self.size = 0
        
        if source_collection is not None:
            for i in source_collection:
                super().add(i)

    def add(self, item):
        '''Add item to the top of the stack.'''
        new_node = node(item)
        new_node.next = self.head
        self.head = new_node
        self.size += 1

    def push(self, item):
        '''Add item to the top of the stack.'''
        self.add(item)

    def extend(self, other):
        '''Add the contents of other to self.'''
        tempstack = stack()
        for i in other:
            tempstack.add(i)
        for j in tempstack:
            self.add(j)
    
    def peek(self):
        '''Return the item at the top of the stack.
        \nPrecondition: the stack is not empty.'''
        if self.isempty():
            raise KeyError('cannot peek an empty stack')   
        return self.head.data
    
    def top(self):
        '''Return the item at the top of the stack.
        \nPrecondition: the stack is not empty.'''
        return self.peek()

    def pop(self):
        '''Remove and return the item at the top of the stack.
        \nPrecondition: the stack is not empty.
        Postcondition: the top item is removed from the stack.'''
        if self.isempty():
            raise KeyError('cannot pop an empty stack')
        backup = self.head.data
        self.head = self.head.next
        if self.size == 1:
            self.tail = None
        self.size -= 1
        return backup

    def __repr__(self):
        return f'stack({str(self)})'
    
    
class queue(chain):
    '''A link-based queue implementation.'''
    def add(self, item):
        '''Add item to the rear of the queue.'''
        super().add(item)

    def push(self, item):
        '''Add item to the rear of the queue.'''
        self.add(item)
    
    def enqueue(self, item):
        '''Add item to the rear of the queue.'''
        self.add(item)

    def peek(self):
        '''Return the item at the front of the queue.
        \nPrecondition: the queue is not empty.'''
        if self.isempty():
            raise KeyError('cannot peek an empty queue')   
        return self.head.data
    
    def front(self):
        '''Return the item at the front of the queue.
        \nPrecondition: the queue is not empty.'''
        return self.peek()        

    def pop(self):
        '''Remove and return the item at the front of the queue.
        \nPrecondition: the queue is not empty.
        \nPostcondition: the front item is removed from the queue.'''
        if self.isempty():
            raise KeyError('cannot pop an empty queue')
        backup = self.head.data
        self.head = self.head.next
        if self.size == 1:
            self.tail = None
        self.size -= 1
        return backup
    
    def dequeue(self):
        '''Remove and return the item at the front of the queue.
        \nPrecondition: the queue is not empty.
        \nPostcondition: the front item is removed from the queue.'''
        return self.pop()
    
    def __repr__(self):
        return f'queue({str(self)})'


class priorityqueue(queue):
    '''A link-based priority queue implementation.'''
    def add(self, item, priority = 0):
        '''Add an item to the queue with a given priority. Lower numbers have higher priority.'''
        new_node = pnode(item, priority = priority)

        if self.isempty():
            self.head = self.tail = new_node
        else:
            # Insert the new node in the correct position based on priority
            if self.head.priority > priority:
                # Insert at the front
                new_node.next = self.head
                self.head = new_node
            else:
                # Traverse to find the correct position
                cur_node = self.head
                while cur_node.next is not None and cur_node.next.priority <= priority:
                    cur_node = cur_node.next
                new_node.next = cur_node.next
                cur_node.next = new_node
                if new_node.next is None:
                    self.tail = new_node

        self.size += 1

    def push(self, item, priority=0):
        '''Add an item to the queue with a given priority. Lower numbers have higher priority.'''
        self.add(item, priority)

    def enqueue(self, item, priority=0):
        '''Add an item to the queue with a given priority. Lower numbers have higher priority.'''
        self.add(item, priority)

    def __repr__(self):
        return f'priorityqueue({str(self)})'


class linklist(chain):
    '''A link-based upgrade to the basic list.'''

    def add(self, item):
        '''Add item to the end of the list.'''
        super().add(item)

    def append(self, item):
        '''Add item to the end of the list.'''
        self.add(item)
    
    def count(self, item):
        '''Return the number of instances of the item in the list.'''
        
        count = 0

        cur_node = self.head
        while cur_node != None:
            if cur_node.data == item:
                count += 1
            cur_node = cur_node.next

        return count
    
    def index(self, item):
        '''Return the position of item.
        \nPrecondition: item is in the list.'''
            
        for i in range(self.size):
            if self[i] == item:
                return i
        raise ValueError(f'{item} is not in list')
    
    def insert(self, i, item):
        '''Insert the item at position i.'''

        if i < 0:
            i = 0
        elif i > self.size:
            i = self.size
        
        new_node = node(item)

        if self.isempty(): #chain is empty
            self.head = new_node
            self.tail = new_node

        elif i == 0: # there are nodes in the chain, and i == 0
            new_node.next = self.head
            self.head = new_node

        elif i == self.size: #inserting new last node
            self.tail.next = new_node
            self.tail = new_node

        else: # inserting somewhere in the middle of the chain
            node_before = self._getnode(i - 1)
            new_node.next = node_before.next
            node_before.next = new_node

        self.size += 1
    
    def pop(self, i = None):
        '''Remove and return the item at position i.
        \nIf i is None, i is given a default of len(self) - 1.
        \nPrecondition: 0 <= i < len(self).'''
        
        if i == None:
            i = self.size - 1
        
        if i < 0 or i >= self.size:
            raise IndexError('index out of range')
        
        if i == 0:
            backup = self.head.data
            self.head = self.head.next
        else:
            prev_node = self._getnode(i - 1)
            node_to_remove = prev_node.next

            backup = node_to_remove.data

            prev_node.next = node_to_remove.next

            if node_to_remove.next == None:
                self.tail = prev_node
      
        self.size -= 1

        return backup
    
    def prepend(self, item):
        '''Add item to the start of the list.'''
        new_node = node(item)
        new_node.next = self.head
        self.head = new_node
        self.size += 1
    
    def pylist(self):
        '''Convert the list into the built-in Python list data type.'''
        new_list = []
        cur_node = self.head
        while cur_node != None:
            new_list.append(cur_node.data)
            cur_node = cur_node.next
        return new_list
   
    def remove(self, item):
        '''Remove the first instance of the item.'''       
        to_remove = self.index(item)
        self.pop(to_remove)

    def removeall(self, item):
        '''Remove all instances of the item.'''
        cur_node = self.head
        i = 0
        while cur_node != None:
            if cur_node.data == item:
                self.pop(i)
                i -= 1
            cur_node = cur_node.next
            i += 1
    
    def replace(self, index, item):
        '''Replace the items at the given position with item.
        \nPreconditions: 0 <= i < len(self)'''
        self[index] = item
    
    def reverse(self):
        '''Reverse the order of elements in the list.'''
        reversed_list = reversed(self)
        self.clear()
        self.extend(reversed_list)
    
    def sort(self, algorithm = None):
        '''Sort the list using one of Cosmic Algorithms's sorting algorithms, or
        Python's built-in sorted() function if one is not provided.'''
        if algorithm is None:
            sortedlist = sorted(self)
        elif not isinstance(algorithm, str):
            raise TypeError('sorting algorithm must be a string')
        else:
            if algorithm.lower() in ('selection', 'selectionsort', 'selection sort'):
                sortedlist = selectionsort(self)
            elif algorithm.lower() in ('insertion', 'insertionsort', 'insertion sort'):
                sortedlist = insertionsort(self)
            elif algorithm.lower() in ('bubble', 'bubblesort', 'bubble sort'):
                sortedlist = bubblesort(self)
            elif algorithm.lower() in ('merge', 'mergesort', 'merge sort'):
                sortedlist = mergesort(self)
            elif algorithm.lower() in ('quick', 'quicksort', 'quick sort'):
                sortedlist = quicksort(self)
            elif algorithm.lower() in ('radix', 'radixsort', 'radix sort'):
                sortedlist = radixsort(self)
            else:
                raise ValueError('invalid sorting algorithm')
        self.clear()
        self.extend(sortedlist)

    def _getnode(self, i): #Helper method
        '''Helper method: Return a pointer to the node at position i.'''
        
        if i < 0 or i >= self.size:
            return None
        
        index = 0
        cur_node = self.head
        while index < i:
            cur_node = cur_node.next
            index += 1
        
        return cur_node
    
    def __array__(self, dtype=None, copy=None):
        '''Convert the linklist to a NumPy array.'''
        return array(self.pylist(), dtype, copy)
    
    def __getitem__(self, i):
        '''Return the item at position i.
        \nPrecondition: 0 <= i < len(self)'''
        
        if isinstance(i, int):
            if i < 0: #Handle negative indices
                i += self.size
            if i < 0 or i >= self.size:
                raise IndexError('index out of range')
            return self._getnode(i).data
        
        elif isinstance(i, slice):
            start, stop, step = i.indices(self.size)
            if start < 0 or stop > self.size or step <= 0:
                raise IndexError('index out of range')
            sliced_list = linklist()
            for index in range(start, stop, step):
                sliced_list.append(self._getnode(index).data)
            return sliced_list

        else:
            raise TypeError('indices must be integers or slices')

    def __setitem__(self, i, item):
        '''Replace the item at position i.
        \nPrecondition: 0 <= i < len(self)'''
        
        if isinstance(i, int):
            if i < 0: #Handle negative indices
                i += self.size
            if i < 0 or i >= self.size:
                raise IndexError('index out of range')
            self._getnode(i).data = item
        else:
            raise TypeError('indices must be integers')
    
    def __str__(self):
        '''Return the string representation of the list.'''
        chain_string = ''
        
        cur_node = self.head
        while cur_node != None:
            chain_string += str(cur_node.data) + ', '
            cur_node = cur_node.next
                    
        chain_string = f'[{chain_string[:-2]}]'
        
        return chain_string

    def __repr__(self):
        return f'linklist({str(self)})'
    
    def __reversed__(self):
        '''Return a reversed copy of the list.'''
        cur_node = self.head
        reversed_list = linklist()
        while cur_node != None:
            reversed_list.prepend(cur_node.data)
            cur_node = cur_node.next
        return reversed_list

class dlinklist(linklist):
    '''A doubly link-based upgrade to the basic list.'''

    def add(self, item):
        '''Add item to the end of the list.'''
        new_node = dlnode(item)

        if self.size == 0:
            self.head = new_node
        else:
            self.tail.next = new_node
        
        new_node.prev = self.tail
        self.tail = new_node
        self.size += 1 

    def append(self, item):
        '''Add item to the end of the list.'''
        self.add(item)
    
    def insert(self, i, item):
        '''Insert the item at position i.'''

        if i < 0:
            i = 0
        elif i > self.size:
            i = self.size
        
        new_node = dlnode(item)

        if self.isempty(): #chain is empty
            self.head = new_node
            self.tail = new_node

        elif i == 0: # there are nodes in the chain, and i == 0
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node

        elif i == self.size: #inserting new last node
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node

        else: # inserting somewhere in the middle of the chain
            node_before = self._getnode(i - 1)
            new_node.next = node_before.next
            new_node.prev = node_before
            node_before.next = new_node
            new_node.next.prev = new_node

        self.size += 1
    
    def pop(self, i = None):
        '''Remove and return the item at position i.
        \nIf i is None, i is given a default of len(self) - 1.
        \nPrecondition: 0 <= i < len(self).'''
        
        if i == None:
            i = self.size - 1
        
        if i < 0 or i >= self.size:
            raise IndexError('index out of range')
        
        if i == 0:
            backup = self.head.data
            self.head = self.head.next
            self.head.prev = None
        else:
            prev_node = self._getnode(i)
            node_to_remove = prev_node.next

            backup = node_to_remove.data

            prev_node.next = node_to_remove.next

            if node_to_remove.next == None:
                self.tail = prev_node
            else:
                node_to_remove.next.prev = prev_node
      
        self.size -= 1

        return backup
    
    def prepend(self, item):
        '''Add item to the start of the list.'''
        new_node = dlnode(item)
        new_node.next = self.head
        self.head.prev = new_node
        self.head = new_node
        self.size += 1

    def __getitem__(self, i):
        '''Return the item at position i.
        \nPrecondition: 0 <= i < len(self)'''
        
        if isinstance(i, int):
            if i < 0: #Handle negative indices
                i += self.size
            if i < 0 or i >= self.size:
                raise IndexError('index out of range')
            return self._getnode(i).data
        
        elif isinstance(i, slice):
            start, stop, step = i.indices(self.size)
            if start < 0 or stop > self.size or step <= 0:
                raise IndexError('index out of range')
            sliced_list = dlinklist()
            for index in range(start, stop, step):
                sliced_list.append(self._getnode(index).data)
            return sliced_list

        else:
            raise TypeError('indices must be integers or slices')

    def __repr__(self):
        return f'dlinklist({str(self)})'

    def __reversed__(self):
        '''Return a reversed copy of the list.'''
        cur_node = self.tail
        reversed_list = dlinklist()
        while cur_node != None:
            reversed_list.append(cur_node.data)
            cur_node = cur_node.prev
        return reversed_list

class tree(object):
    '''A link-based representation of a general tree. Can also represent an
    n-ary tree where n is defined by the max_children parameter.'''

    def __init__(self, root_data = None, max_children = None):
        if not isinstance(max_children, int) and max_children is not None:
            raise TypeError('max_children must be an int')
        self.max_children = max_children
        if root_data is None:
            self.root = None
        else:
            self.root = tnode(root_data, [], self.max_children)

    def isbinary(self):
        '''Return True if the tree is a binary tree, False otherwise.'''
        return self.max_children == 2
    
    def isempty(self):
        '''Return True if the tree is empty, False otherwise.'''
        return self.root is None
        
    def add(self, item, parent = None):
        '''Add an item to the tree.'''
        if parent is None:
            if self.root is None:
                self.root = tnode(item, [], self.max_children)
            else:
                raise ValueError('tree already has a root')
        elif parent == self.root:
            if self.root is None:
                raise ValueError('cannot add child to a non-existent root')
            self.root.add(item)
        else:
            target = self.findnode(parent.data if isinstance(parent, tnode) else parent)
            if target is None:
                raise ValueError('the specified parent is not in the tree')
            target.add(item)

    def findnode(self, target, node = None):
        '''Find the first instance of the target in the tree.'''
        if node is None:
            node = self.root
        if node is None:
            return None
        if node.data == target:
            return node
        for child in node.children:
            found = self.findnode(target, child)
            if found:
                return found
        return None
    
    def remove(self, target):
        '''Remove a node with the given target data from the tree.'''
        if self.isempty():
            raise ValueError('cannot remove from an empty tree')

        # Special case: if the root is the target
        if self.root.data == target:
            self.root = None
            return

        # Helper function to find and remove the target node
        def _removehelper(node, target):
            for i, child in enumerate(node.children):
                if child.data == target:
                    # Remove the child and break the parent reference
                    removed_node = node.children.pop(i)
                    removed_node.parent = None
                    return True
                # Recursively check the child's children
                if _removehelper(child, target):
                    return True
            return False

        # Start the removal process from the root
        if not _removehelper(self.root, target):
            raise ValueError(f'{target} is not in the tree')
        
    def preorder(self, node=None):
        '''Conduct a preorder traversal of the tree.
        \nVisit the current node before its children.'''
        if node is None:
            node = self.root
        if node is None:
            return []
        result = [node.data]  # Visit the current node
        for child in node.children:
            result.extend(self.preorder(child))  # Recursively visit children
        return result

    def postorder(self, node=None):
        '''Conduct a postorder traversal of the tree.
        \nVisit the children of the current node before the node itself.'''
        if node is None:
            node = self.root
        if node is None:
            return []
        result = []
        for child in node.children:
            result.extend(self.postorder(child))  # Recursively visit children
        result.append(node.data)  # Visit the current node
        return result
    
    def height(self, node=None):
        '''Return the height of the tree.
        \nThe height is the number of edges on the longest path from the node to a leaf.'''
        if node is None:
            node = self.root
        if node is None:
            return -1  # By convention, the height of an empty tree is -1
        if node.isleaf():
            return 0  # A leaf node has a height of 0
        return 1 + max(self.height(child) for child in node.children)
        
    def __contains__(self, target):
        '''Return True if the tree contains the node, False otherwise.'''
        return (self.findnode(target, self.root) is not None)

    def __len__(self):
        '''Return the number of nodes in the tree.'''
        return self.size
    
    def __str__(self):
        '''Return the string representation of the tree.'''
        return_string = ''
        if self.max_children is not None:
            return_string += str(self.max_children)
        if self.isempty():
            return_string += '[]'
        else:
            return_string += f'[{self.root}]'
        return return_string