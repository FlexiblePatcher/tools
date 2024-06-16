class Segment:
    def __init__(self, start=None, count=None):
        self.start = start
        self.count = count


class Variable:
    def __init__(self):
        self.initializer = []
        self.segment = []

    def next_start(self):
        if not self.segment:
            return 0
        last_segment = self.segment[-1]
        return last_segment.start + last_segment.count

    def add_segment(self):
        start = self.next_start()
        self.segment.append(Segment(start, len(self.initializer) - start))

    def segment_definition(self, name):
        return 'const array_segment {}_segment[{}] = {{{}}};\nconst int {}_segment_size = {};\n'.format(name, len(self.segment) if self.segment else 1, ', '.join(['{{{}, {}}}'.format(current_segment.start, current_segment.count) for current_segment in self.segment]), name, len(self.segment))

    def definition(self, type, name):
        return 'const {} {}[{}] = {{{}}};\nconst int {}_size = {};\n'.format(type, name, len(self.initializer) if self.initializer else 1, ', '.join(self.initializer), name, len(self.initializer)) + self.segment_definition(name)
