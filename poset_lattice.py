'''
Need improvement from the code and knowledge is used to built this.
Sorry for the readableness and the quality of code not as your expectation.
'''

import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations


# return GCD from pair of nums by modulating the nums iteratively.
def gcd(a, b):
    while b > 0:
        a, b = b, a % b
    return a


def lcm(a, b):
    return a * b / gcd(a, b)


def unique(seq):
    seen = {}
    pos = 0
    for item in seq:
        if item not in seen:
            seen[item] = True
            seq[pos] = item
            pos += 1
    del seq[pos:]


# Parent class, define and relationing input of a set.
class definerSet:
    def __init__(self, setInput):
        self.raw = setInput
        self.raw.sort()
        self.rawCombs = [x for x in combinations(self.raw, 2)]
        self.relation = list()
        self.rTypes = {0: "Divisible"}
        self.rChosen = None
        self.isPoset = None
        self.isLattice = None

        self.hasse = hasse(definerSet=self)

    # Generate pair of divisible relation from Input.
    def rDivisible(self):
        self.rChosen = 0
        unique(self.raw)

        self.relation = [(divisor, num)
                         for divisor in self.raw
                         for num in self.raw
                         if num % divisor == 0]

    def rWhat(self):
        return self.rTypes[self.rChosen]

    # For not directly pointing to private variable.
    def getter(self, fromVar):
        return fromVar


# Subclass, to do hasse things.
class hasse:
    def __init__(self, definerSet):
        self.definerSet = definerSet
        self.hDiagram = nx.DiGraph()

        self.sortOut = sortOut(hasse=self)

    def Sortedf(self):
        return self.sortOut.degreeOut()

    # Draw hasse diagram by rules.
    def draw(self):
        assert self.definerSet.isPoset is True
        self.hDiagram.add_edges_from(self.sortOut.degreeOut())

        print('Sorry too slow,')

        if self.definerSet.isLattice is True:
            iLattie = "Lattice"
        elif self.definerSet.isLattice is False:
            iLattie = "Not a Lattice"

        type = '{} Hasse Digram [{}]'.format(iLattie, self.definerSet.rWhat())
        plt.title(type)

        # pos = nx.circular_layout(h)
        pos = nx.spring_layout(self.hDiagram)
        nx.draw(self.hDiagram,
                pos,
                with_labels=True,
                node_color='r',
                edge_labels=True)

        plt.show()


# Subclass of hasse, Sorting wrapper.
class sortOut(hasse):
    def __init__(self, hasse):
        self.hasse = hasse

    # Compare its own without reflective pair.
    @staticmethod
    def ruleR(from_set, target_set):
        for (a, b), (c, d) in combinations(from_set, 2):
            if a != b and c != d:
                if all(r in target_set for r in ((a, b), (c, d), (b, d))):
                    yield (a, b, c, d)


    # Remove unneeded transitive pair
    # if b ≤ d and no p ∈ rule1 so that b ≤ p and p ≤ d.
    def ruleOut(self):
        rule = self.hasse.definerSet.getter(self.hasse.definerSet.relation)

        for a, b, c, d in sortOut.ruleR(self.hasse.definerSet.relation, rule):
            if a == c:
                rule.remove((c, d))

        return rule

    # Choose the most lower degree if 0 ≤ a and 0 ≤ c.
    def degreeOut(self):
        '''
        This loop has a bug if the same count of degree arise,
        I don't have reliable knowledge to do it right,
        Sorry, and I really appreciate if someone could fix it.
        '''

        rule1 = rule2 = self.ruleOut()
        count_a = count_c = 0

        for a, b, c, d in sortOut.ruleR(rule1, rule2):
            if b == d:
                for i, j in rule2:
                    if i == a:
                        count_a += 1
                    elif i == c:
                        count_c += 1

                if count_a > count_c:
                    rule2.remove((a, b))
                elif count_c > count_a:
                    rule2.remove((c, d))

                # Need a fix.
                elif (count_a + count_c) != 4 and count_a == count_c:
                    if a > c:
                        rule2.remove((c, d))
                    elif c > a:
                        rule2.remove((a, b))

                count_a = count_c = 0

        # print('rule1', rule1)
        # print('rule2', rule2)
        return rule2


# Subclass, to do poset things.
class poset(definerSet):
    def __init__(self, definerSet):
        self.definerSet = definerSet

        self.laws = {'Reflective': self.reflective(),
                     'Antisimetric': self.antisimetric(),
                     'Transitive': self.transitive()}

        self.definerSet.isPoset = self.isItPoset()

        self.bounds = bounds(poset=self)

    def getter(self, fromVar):
        return fromVar

    def __repr__(self):
        if self.Poset is False:
            return("Not a Poset.")

    # Return True if every pair of element ∈ self.definerSet.raw reflective.
    def reflective(self, rlist=False):
        aRa = [a for a, b in self.definerSet.relation if a == b]

        if rlist is True:
            return aRa

        if len(aRa) == len(self.definerSet.raw):
            return True
        else:
            return False

    # Return True if atleast has a pair by if aRb and cRd, a = b and b = c.
    def antisimetric(self, rlist=False):
        aRb = [(a, c) for a, b in self.definerSet.relation
               for c, d in self.definerSet.relation
               if a == d and b == c]

        if rlist is True:
            return aRb

        if len(aRb) > 0:
            return True
        else:
            return False

    # Return True if aRb and cRd, b = c,
    # so that aRc, in every pair of element ∈ self.definerSet.raw.
    def transitive(self, rlist=False):
        for a, b in self.definerSet.relation:
            for c, d in self.definerSet.relation:
                if b == c:
                    if ((a, d) not in self.definerSet.relation):
                        print('For', (a, d), 'from', (a, b),
                              'and', (c, d), 'not in Set.')
                        return False

        if rlist is True:
            return self.definerSet.relation

        return True

    # True if all of 3 laws are True.
    def isItPoset(self):
        if all(self.laws.values()):
            return True
        else:
            return False

# Subclass of poset, infimum & supremum wrapper.
class bounds(poset):
    '''
    Algorithm too slow, is there any efficient way or formula to do it?
    Bug arise when comparing transitive relations that should not be is.
    '''
    def __init__(self, poset):
        self.poset = poset
        self.definerSet = self.poset.definerSet

    def comBs(self, a, b):
        for (i, j), (k, l) in combinations(self.definerSet.relation, 2):
            yield i, j, k, l

    # Supremum, yield true when j is the most closer to a and b while exist in self.definerSet.raw.
    def _leastUpper(self):
        for a, b in self.definerSet.rawCombs:
            last = None
            for i, j, k, l in self.comBs(a, b):
                if i == a and k == b:
                    if j == l:
                        last = True
                        yield last
                        break
            if last is not True:
                yield False

    #Return j, For each X that is another upper bound of (a, b), applies j ≤ X.
    def leastUpper(self, compara=None):
        if compara is None:
            return self._leastUpper()

        elif compara is not None:
            for a, b in [compara]:
                for i, j, k, l in self.comBs(a, b):
                    if i == a and k == b:
                        if j == l:
                            return j
            return None

    # Infimum, yield true when j is the most closer to a and b while exist in self.definerSet.raw.
    def _greatestLower(self):
        for a, b in self.definerSet.rawCombs:
            last = None
            for i, j, k, l in self.comBs(a, b):
                if j == a and l == b:
                    if i == k:
                        last = True
                        yield last
                        break
            if last is not True:
                yield False

    #Return i, For each X that is another lower bound of (a, b), applies X ≤ i.
    def greatestLower(self, compara=None):
        if compara is None:
            return self._greatestLower()
        elif compara is not None:
            for a, b in [compara]:
                for i, j, k, l in self.comBs(a, b):
                    if j == a and l == b:
                        if i == k:
                            return i
            return None


# Subclass, to do lattice things. for now, only support divisible lattice.
class lattice(poset):
    def __init__(self, poset):
        self.poset = poset
        self.definerSet = self.poset.definerSet
        self.definerSet.isLattice = self.isItLattice()
        self.irreducible = irreducible(lattice=self)
        if self.definerSet.isLattice is False:
            print("This Works should be Lattice Only.")

    def __repr__(self):
        if self.definerSet.isLattice is False:
            return("Not a Lattice.")

    # infimum(a,b) and supremum (a,b) of self.poset is exist for each pair of elements a and b in self.definerSet.raw.
    def isItLattice(self):
        if all(self.poset.bounds.leastUpper()) and all(self.poset.bounds.greatestLower()):
            return True
        else:
            return False

    # Compare by its own lcm and gcd if match to the smallest & biggest element.
    def complement(self, arg=None):
        complements = []
        if arg is not None:
            for a in self.definerSet.raw:
                if lcm(a, arg) == self.definerSet.raw[-1] and gcd(a, arg) == self.definerSet.raw[0]:
                    return True

            return False

        elif arg is None:
            for a, b in self.definerSet.rawCombs:
                if lcm(a, b) == self.definerSet.raw[-1] and gcd(a, b) == self.definerSet.raw[0]:
                    complements.append((a, b))

            return complements


# Compare gcd & lcm to find meet irreducible and join irreducible.
class irreducible(lattice):
    def __init__(self, lattice):
        self.lattice = lattice
        self.definerSet = self.lattice.definerSet

    def meet(self, arg):
        for a, b in self.definerSet.rawCombs:
            if gcd(a, b) in (a, b):
                if arg in (a, b):
                    return True
        return False

    def join(self, arg):
        for a, b in self.definerSet.rawCombs:
            if lcm(a, b) in (a, b):
                if arg in (a, b):
                    return True
        return False
