class Model:

    def __init__(self):
        self.naive_model = "No Model"
        self.logistic_model = "No Model"
        self.k_neighbors_model = "No Model"
        self.word_indices = "No Words"

    def set_naive_model(self, naive_model):
        self.naive_model = naive_model

    def set_logistic_model(self, logistic_model):
        self.logistic_model = logistic_model

    def set_k_neighbors_model(self, k_neighbors_model):
        self.k_neighbors_model = k_neighbors_model

    def set_word_indices(self, word_indices):
        self.word_indices = word_indices

    def get_naive_model(self):
        return self.naive_model

    def get_logistic_model(self):
        return self.logistic_model

    def get_k_neighbors_model(self):
        return self.k_neighbors_model

    def get_word_indices(self):
        return self.word_indices
