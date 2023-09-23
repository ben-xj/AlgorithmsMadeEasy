import random
from typing import Protocol


class AcceptCriterion(Protocol):
    
    def accept(self, cur, new):
        """
        whether to accept a new solution, returns True for acception
        """

class HillClimbing:

    def accept(self, cur, new):
        return new <= cur
    
class SimulatedAnnealing:

    def __init__(self, init_T, rate):
        self.temperature = init_T
        self.rate = rate
    
    def update_temperature(self):
        self.temperature *= self.rate
    
    def accept(self, cur, new):
        sa_prob = (cur - new) / self.temperature
        return random.random() <= sa_prob