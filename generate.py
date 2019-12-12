from collections import defaultdict
import random

class PCFG(object):
    def __init__(self):
        self._rules = defaultdict(list)
        self._sums = defaultdict(float)

    def add_rule(self, lhs, rhs, weight):
        assert(isinstance(lhs, str))
        assert(isinstance(rhs, list))
        self._rules[lhs].append((rhs, weight))
        self._sums[lhs] += weight

    @classmethod
    def from_file(cls, filename):
        grammar = PCFG()
        with open(filename) as fh:
            for line in fh:
                line = line.split("#")[0].strip()
                if not line: continue
                w,l,r = line.split(None, 2)
                r = r.split()
                w = float(w)
                grammar.add_rule(l,r,w)
        return grammar

    def is_terminal(self, symbol): return symbol not in self._rules

    def gen(self, symbol,printTrees):
        if self.is_terminal(symbol): return symbol
        else:
            expansion = self.random_expansion(symbol)
            output = " ".join(self.gen(s,printTrees) for s in expansion)
            if printTrees:
                return "(" + symbol + " " + output + ")"
            return output
            

    def random_sent(self,printTrees):
        return self.gen("ROOT",printTrees)

    def random_expansion(self, symbol):
        """
        Generates a random RHS for symbol, in proportion to the weights.
        """
        p = random.random() * self._sums[symbol]
        for r,w in self._rules[symbol]:
            p = p - w
            if p < 0: return r
        return r
           
def createParams(argv):
        params = {}
        for i,obj in enumerate(argv):
            if obj == '-t':
                params[obj] = 1
            if obj == '-n':
                params[obj] = argv[i + 1]
        return params 
    
if __name__ == '__main__':
    import sys
    pcfg = PCFG.from_file(sys.argv[1])
    params = createParams(sys.argv)
    printTrees = True if "-t" in sys.argv else False
    
    if "-n" in params:
        for i in range(int(params["-n"])):
            print(pcfg.random_sent(printTrees))
    else:
        print(pcfg.random_sent(printTrees))
