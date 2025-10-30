from collections import defaultdict

class PrefixTree(object):

    r"""
    Prefix Tree or Trie class. Creates a tree structure where each node is a letter.
    Traversing the tree to a leaf will spell a unique valid word.

    For example this is a PrefixTree containing 3 words: BAT, TREE, and TRY
         ROOT
        /    \ 
        B     T
        |     |
        A     R
        |    / \  
        T    E  Y
             |
             E
    
    Each node contains the tree structure below it. Each node also has an
    attribute "prefix" that contains the letters in the path followed to reach
    that node. A boolean value "is_word" denotes that this nodes prefix is a 
    valid word. Valid words may also have children. For example, RUN is a valid 
    word with child words RUNS, RUNNING, RUNNER, etc.
    """

    def __init__(self, words: list[str]):
        self.prefix = '' # Root prefix is empty string
        self.is_word = False
        self.edges = defaultdict(lambda: self.__class__([]))
        self._word_count = 0
        for word in words:
            self.add_word(word, depth=0)

    def add_word(self, word: str, depth: int = 0):
        """
        Add a word segment to this node.

        Arguments:
            word: The complete word being added
            n: The current depth of this node
        """
        self.prefix = word[:depth]
        self._word_count += 1
        if self.prefix == word:
            self.is_word = True
        else:
            self.edges[word[depth]].add_word(word, depth=depth+1)
    
    def __getitem__(self, prefix: str):
        """
        Traverse tree downwards following letters in prefix. Return a sub-tree
        containing words starting with the prefix, or KeyError if no such words
        exist in the tree.

        For example, for a prefix tree loaded with common English words.
        pt['TH'] returns a sub-tree containing all words starting with TH
        pt['ZZZWXQK'] raises a KeyError
        """
        if prefix[0] in self.edges:
            if len(prefix) <= 1:
                return self.edges[prefix[0]]
            else:
                return self.edges[prefix[0]][prefix[1:]]
        else:
            raise KeyError(prefix)
    
    def __contains__(self, prefix: str):
        """
        Check if words beginning with prefix exist in the tree, including if
        prefix is a leaf node.
        """
        if len(prefix) <= 1:
            return prefix in self.edges
        else:
            return prefix[1:] in self.edges[prefix[0]]

    def get(self, *args):
        """
        Emulates dict.get
        """
        try:
            self[args[0]]
        except KeyError:
            return args[1] if len(args)>=2 else None

    def __iter__(self):
        """
        Yield all valid words from this node
        """
        if self.is_word:
            yield self
        for child in self.edges.values():
            yield from child

    def __len__(self):
        """
        Count of valid words from this node
        """
        return self._word_count