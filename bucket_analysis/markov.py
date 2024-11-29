import numpy as np
import utils

class MarkovChain:

    """
    Represents an executable Markov Chain.
    """

    def __init__(self, initial_state_distributions, transition_distributions, iteration_count = 1):
        """        
        Attributes:
            initial_state_distribution (dict): Mapping of state name -> probability, used for the initial state. Automatically normalized as needed.
            transition_distribution (dict): Mapping of state transitions.  map[src, map[dst, prob]]. Automatically normalized as needed.
        """        
        self._initial_states = utils.normalize(initial_state_distributions)
        self._transitions = {k: utils.normalize(v) for k, v in transition_distributions.items()}
        self._iteration_count = iteration_count

    def run(self) -> list:
        """
        Run the Markov Chain according to the parameters and return the list of states.
        """
        states = []
        current_state = np.random.choice(list(self._initial_states.keys()), p=list(self._initial_states.values()))
        states.append(str(current_state))

        for i in range(self._iteration_count):
            transition_probs = self._transitions[current_state]
            next_state = np.random.choice(list(transition_probs.keys()), p=list(transition_probs.values()))
            current_state = str(next_state)
            states.append(current_state)

        return states
    
    
    

