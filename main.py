from poset_lattice import *
import random
import traceback
from functools import reduce

def factors(n):
    return set(reduce(list.__add__,
                ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0)))

def main():
    exampleInfo = ['Lattice-Complete', 'Non-Supremum\t', 'Non-Infimum\t']
    example = {0: [1, 2, 3, 4, 6, 9, 12, 18, 36], # Lattice-Complete
               1: [1, 3, 2, 6, 12, 24, 36],       # Non-Supremum
               2: [2, 3, 6, 12, 24, 48]}          # Non-Infimum

    print("For Easy Copy:")
    for i, e in example.items():
        print(exampleInfo[i] + "\t:", ", ".join(repr(x) for x in e))
    print('\n')

    # listS = example[0]
    # listS = list(factors(48))
    listS = [int(x) for x in input("Some random elements: ").split(',')]

    ds = definerSet(listS)
    ds.rDivisible()

    p_ds = poset(ds)
    for law, val in p_ds.laws.items():
        print(law, "\t:", val)
    print('Is a Poset?', ds.isPoset)

    nums = (3, 6)
    print('Least Upper Bound of', nums, 'is', p_ds.bounds.leastUpper(nums))
    print('Greatest Lower Bound of', nums, 'is', p_ds.bounds.greatestLower(nums))

    l_ds = lattice(p_ds)
    print('Is a Lattice?', ds.isLattice)

    number = 9
    print('Is %d Meet Irreducible\t:' % number, l_ds.irreducible.meet(number))
    print('Is %d Join Irreducible\t:' % number, l_ds.irreducible.join(number))
    print('Complements\t:', l_ds.complement())
    ds.hasse.draw()


if __name__ == '__main__':
    while 1:
        try:
            while 1:
                print("="*90)
                main()
                print("="*90, "\n")
        except Exception:
            traceback.print_exc()
            pass
        else:
            break
