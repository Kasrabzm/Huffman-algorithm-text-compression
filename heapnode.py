class HeapNode():
    def __init__(self, char, frequency, left=None, right=None):
        self.char = char
        self.frequency = frequency
        self.left = left
        self.right = right

    def __gt__(self, other):
        assert type(other) == HeapNode
        return self.frequency > other.frequency

    def __lt__(self, other):
        assert type(other) == HeapNode
        return self.frequency < other.frequency

    def __eq__(self, other):
        if type(self) == type(other):
            return True
        elif type(self) != type(other):
            return False

    def __ne__(self, other):
        if type(self) == type(other):
            return False
        elif type(self) != type(other):
            return True

    def __ge__(self, other):
        assert type(other) == HeapNode
        return self.frequency >= other.frequency

    def __le__(self, other):
        assert type(other) == HeapNode
        return self.frequency <= other.frequency
