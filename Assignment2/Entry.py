class Entry:
    attributes = []
    attribute_length = 0
    result = None
    distance = 0

    def __init__(self, attributes, result):
        self.attributes = attributes
        self.result = result
        self.attribute_length = len(attributes)

    def get_attribute(self, index):
        num = float(self.attributes[index])
        return num

    def get_attribute_length(self):
        return self.attribute_length

