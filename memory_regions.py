class Region:
    def __init__(self, start=None, size=None, number=None, name=None, entry=None, index=None):
        self.start = start
        self.size = size
        self.number = number
        self.name = name
        self.entry = entry
        self.index = index

    def overlap(self, region):
        return self.start < region.start + region.size and self.start + self.size > region.start

    def to_string(self):
        return '{} [{}] [{}]'.format(self.name, self.entry, self.index)
