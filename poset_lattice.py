import networkx as nx
import matplotlib.pyplot as plt

# return GCD from pair of nums by modulating the nums iteratively.
def gcd(a, b):
    while b > 0:
        a, b = b, a % b
    return a

# return LCM from pair of nums.
def lcm(a, b):
    return a * b / gcd(a, b)


# Parent class, define and relationing input of a set.
class definerSet:
    def __init__(self, setInput):
        self.raw = setInput
        self.raw.sort()
        self.relation = list()

    # Generate pair of divisible relation from Input.
    def Rdivisible(self):
        self.relation = [(divisor, num)
                         for divisor in self.raw
                         for num in self.raw
                         if num % divisor == 0]


# Subclass, to do hasse things.
class hasse:
    def __init__(self, definerSet):
        self.definerSet = definerSet
        self.poset = poset(definerSet)
        self.lattice = lattice(definerSet)

    # Draw hasse diagram by rules.
    def draw(self):
        h = nx.DiGraph()

        if self.poset.isPoset() is True:

            # Compare its own without reflective pair.
            def rule_sorter(from_set, target_set):
                for a, b in from_set:
                    if (a, b) in target_set and a != b:
                        for c, d in from_set:
                            if (c, d) in target_set and c != d:
                                if (a, b) != (c, d):
                                    yield (a, b, c, d)

            rule1 = [x for x in self.definerSet.relation]

            # Remove unneeded transitive pair if b ≤ d and no p ∈ rule1 so that b ≤ p and p ≤ d.
            for a, b, c, d in rule_sorter(self.definerSet.relation, rule1):
                if a == c and (b, d) in self.definerSet.relation:
                    rule1.remove((c, d))

            rule2 = [x for x in rule1]

            '''
            This loop has a bug if the same count of degree arise,
            I don't know what should I do and what is right to do,
            don't have reliable knowledge to fix it.
            Sorry, and I really really appreciate if someone could fix it.
            '''
            # Choose the most lower degree if 0 ≤ a and 0 ≤ c.
            count_a, count_c = 0, 0
            for a, b, c, d in rule_sorter(rule1, rule2):
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

                    count_a, count_c = 0, 0

            # print('rule1', rule1)
            # print('rule2', rule2)
            h.add_edges_from(rule2)

        elif self.poset.isPoset() is False:
            print("Not a poset")

        print('Regret not In the rIght tIme :(')

        check = self.lattice.isLattice()
        if check[0] is True:
            type = 'Lattice Hasse Digram [{}]'.format(check[1])
        elif check[0] is False:
            type = 'not a Lattice Hasse Digram [{}]'.format(check[1])

        plt.title(type)

        pos = nx.spring_layout(h)
        # pos = nx.circular_layout(h)
        nx.draw(h, pos, with_labels=True, node_color='r', edge_labels=True)

        plt.show()


# Subclass, to do poset things.
class poset(definerSet):
    def __init__(self, definerSet):
        self.definerSet = definerSet

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

    # Return True if aRb and cRd, b = c, so that aRc, in every pair of element ∈ self.definerSet.raw.
    def transitive(self, rlist=False):
        for a, b in self.definerSet.relation:
            for c, d in self.definerSet.relation:
                if b == c and ((a, d) not in self.definerSet.relation):
                    print((a, b), 'and', (c, d), 'not transitive')
                    return False

        if rlist is True:
            return self.definerSet.relation

        return True

    # True if all of 3 laws are True.
    def isPoset(self):
        laws_str = ['Reflective', 'Antisimetric', 'Transitive']
        laws = [self.reflective(),
                self.antisimetric(),
                self.transitive()]

        if laws == [True] * 3:
            return True
        else:
            return False


# Subclass, to do lattice things. for now, only support divisible lattice.
class lattice:
    def __init__(self, definerSet):
        self.definerSet = definerSet
        self.poset = poset(definerSet)

    # Check if its what lattice or not.
    def isLattice(self):
        for a in self.definerSet.raw:
            for b in self.definerSet.raw:
                if gcd(a, b) not in self.definerSet.raw or lcm(a, b) not in self.definerSet.raw:
                    return (False, 'divisible')

        return (True, 'divisible')

    # Compare gcd & lcm to find meet irreducible and join irreducible by switch arg.
    def irreducible(self, option):
        mj = []

        if self.isLattice()[0] is True:

            for a in self.definerSet.raw:
                for b in self.definerSet.raw:

                    if option == 0:
                        meet_join = gcd(a, b)

                    elif option == 1:
                        meet_join = lcm(a, b)

                    if meet_join == a or meet_join == b:
                        mj.append((a, b))

            return mj

        elif self.isLattice()[0] is False:
            return (None, 'non-Divisible Lattice will be on works.')

    def meet_irreducible(self):
        return self.irreducible(0)

    def join_irreducible(self):
        return self.irreducible(1)

    # Compare arg by its own lcm and gcd if match to the smallest & biggest element.
    def complement(self, arg=None):
        cl = []
        if self.isLattice()[0] is True:
            for a in self.definerSet.raw:
                if arg is not None:
                    if lcm(a, arg) == self.definerSet.raw[-1] and gcd(a, arg) == self.definerSet.raw[0]:
                        return True
                    else:
                        return False

                elif arg is None:
                    for b in self.definerSet.raw:
                        if lcm(a, b) == self.definerSet.raw[-1] and gcd(a, b) == self.definerSet.raw[0]:
                            cl.append((a, b))

        return cl        
