import random

class App:
    def __init__(self,width, height):
        self.counts = {'H':1, 'T':1}
        self.width, self.height = width, height

    def generate_prediction(self, probability_for_head=0.5):
        probability = random.uniform(0, 1)
        if probability<=probability_for_head:
            self.counts['H']+=1
        else:
            self.counts['T']+=1


