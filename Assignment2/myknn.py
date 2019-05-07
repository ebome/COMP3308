import math


class KNN:
    k = 0
    training_entries = []
    neighbour = []

    def __init__(self, k, training):
        self.k = k
        self.training_entries = training

    def compute_distance(self, new_entry):
        for e in self.training_entries:
            sum_of_eu = 0
            for j in range(0, e.get_attribute_length()):
                sum_of_eu += math.pow((e.get_attribute(j) - new_entry.get_attribute(j)), 2)

            result = math.sqrt(sum_of_eu)
            e.distance = result

        self.training_entries.sort(key=lambda x: x.distance, reverse=False)
        for i in range(0, self.k):
            self.neighbour.append(self.training_entries[i])
            # print(self.training_entries[i].attributes, self.training_entries[i].distance, self.training_entries[i].result)

        return self.neighbour

