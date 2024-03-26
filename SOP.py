import numpy as np
import matplotlib.pyplot as plt


class Node:
    def __init__(self, I=1, A1=0, A2=0, w1=1, w2=0, p1=0.9, pd1=0.1, pd2=0.02, C1=2, C2=10, Lplus=0.1, Lminus=0.01, learning=1,  r1=1, r2=0):
        if not all(0 <= param <= 1 for param in [I, A1, A2, p1, pd1, pd2,Lplus,Lminus,learning]):
            raise ValueError("All parameters must be between 0 and 1")
        
        if I + A1 + A2 != 1:
            raise ValueError("The sum of the values I, A1 and A2 must be equal to 1")
        
        self.I = np.array([I])
        self.A1 = np.array([A1])
        self.A2 = np.array([A2])
        self.w1 = w1
        self.w2 = w2
        
        self.p1 = p1
        self.pd1 = pd1
        self.pd2 = pd2
        
        self.pd1_prime = np.array([0])
        self.pd2_prime = np.array([0])
        self.distractors = []
        self.C1 = C1
        self.C2 = C2
        
        self.V = {}
        self.Lplus = Lplus
        self.Lminus = Lminus
        self.learning = learning
        
        self.p2 = np.array([0])
        self.r1 = r1
        self.r2 = r2

        self.stimuli = []
        self.response = np.array([0])

    def associate(self, nodes):
        if not isinstance(nodes, list):
            nodes = [nodes]
        
        if not all(isinstance(node,Node) for node in nodes):
            raise TypeError("All arguments must be Nodes")

        for node in nodes:
            self.V[node] = np.array([0])

    def distractor(self, nodes):
        if not isinstance(nodes, list):
            nodes = [nodes]
        
        if not all(isinstance(node,Node) for node in nodes):
            raise TypeError("All arguments must be Nodes")

        for node in nodes:
            self.distractors.append(node)

    def response_generator(self,w1,w2):
        self.response = w1*self.A1 + w2*self.A2
    
    def update(self,moment):
        stimulus = 1 if moment in self.stimuli else 0
        
        dI = self.A2[moment]*self.pd2_prime[moment] - self.I[moment]*self.p1*stimulus - self.I[moment]*self.p2[moment]
        self.I = np.concatenate([self.I, [self.I[moment] + dI]])
        
        dA1 = self.I[moment]*self.p1*stimulus - self.A1[moment]*self.pd1_prime[moment]
        self.A1 = np.concatenate([self.A1, [self.A1[moment] + dA1]])

        dA2 = self.A1[moment]*self.pd1_prime[moment] + self.I[moment]*self.p2[moment] - self.A2[moment]*self.pd2_prime[moment] 
        self.A2 = np.concatenate([self.A2, [self.A2[moment] + dA2]])

        #Check if there is any association
        if self.V:
            association_sum = 0
        
            for node in self.V:
                dV = self.learning*node.A1[moment]*(self.A1[moment]*self.Lplus - self.A2[moment]*self.Lminus)
                self.V[node] = np.concatenate([self.V[node],[self.V[node][moment] + dV]])
                association_sum += (self.r1*node.A1[moment] + self.r2*node.A2[moment])*self.V[node][moment]

            p2 = max(min(association_sum,1),0)
            self.p2 = np.concatenate([self.p2, [p2]])
        else:
            self.p2 = np.concatenate([self.p2,[0]])

        #Check if there is any distractor
        if self.distractors:   

            self.pd1_prime = np.concatenate([self.pd1_prime,[self.pd1 + sum([node.A1[moment] for node in self.distractors])/self.C1]])
            self.pd2_prime = np.concatenate([self.pd2_prime,[self.pd2 + sum([node.A2[moment] for node in self.distractors])/self.C2]])
        else:
            self.pd1_prime = np.concatenate([self.pd1_prime,[self.pd1]])
            self.pd2_prime = np.concatenate([self.pd2_prime,[self.pd2]])

        self.response = np.concatenate([self.response,[self.w1*self.A1[moment] + self.w2*self.A2[moment]]])

class Experiment:
    def __init__(self, time, nodes):
        
        self.time = list(range(0,time+1))

        self.number_of_trials = {}
        self.trials = {}

        self.number_of_tests = {}
        self.tests = {}

        self.number_of_stimuli = {}
        self.stimuli = {}
        
        self.nodes = nodes

    def define_trials(self, number_of_trials, ISI, nodes, start_at=0, stimulus_duration=1):
        if not isinstance(nodes, list):
            nodes = [nodes]
        
        if not all(isinstance(node,Node) for node in nodes):
            raise TypeError("Error. The list of nodes contain one or more objects that aren't Nodes.")
        
        #if node not in self.nodes for node in nodes:
         #   raise TypeError("Error. You must use a node associated to this experiment.")

        for node in nodes:
            self.number_of_trials[node] = number_of_trials
            trials = []
            
            for i in range(number_of_trials):
                for j in range(stimulus_duration):
                    trials.append(start_at+(ISI+stimulus_duration*1)*i+j)
            
            self.trials[node] = trials
            node.stimuli += [trial for trial in trials]
    
    def define_tests(self, nodes, tests_at=[],stimulus_duration=1): 
        if not isinstance(nodes, list):
            nodes = [nodes]
        
        if not all(isinstance(node,Node) for node in nodes):
            raise TypeError("Error. The list of nodes contain one or more objects that aren't Nodes.")
        
        #if node not in self.nodes for node in nodes:
         #   raise TypeError("Error. You must use a node associated to this experiment.")        

        for node in nodes:
            self.number_of_tests[node] = len(tests_at)
            tests = []
            
            if type(tests_at) == int:
                tests_at = [tests_at] 
            
            for t in tests_at:
                for i in range(stimulus_duration):
                    tests.append(self.trials[node][-1]+t+i+1)

            self.tests[node] = tests
            node.stimuli += tests
            
            self.number_of_stimuli[node] = len(node.stimuli)
            self.stimuli[node] = node.stimuli
        
        
        
    def stimulus_generator(self, trials, ISI, stimulus_duration, nodes, prestimulus_interval=0):
        print("SS")                                                                                                   

    def run(self):
        if not isinstance(self.nodes, list):
            self.nodes = [self.nodes]
        
        for moment in self.time:
            for node in self.nodes:
                node.update(moment)
        

