import poset_lattice as pl
import random

def main():
    list = [1, 2, 3, 4, 6, 9, 12, 18, 36]
    ds = pl.definerSet(list)
    ds.Rdivisible()

    p_ds = pl.poset(ds)
    reflective = p_ds.reflective(rlist=False)
    antisimetric = p_ds.antisimetric(rlist=False)
    transitive = p_ds.transitive(rlist=False)

    hp = pl.hasse(ds)
    hp.draw()

    l_ds = pl.lattice(ds)

    print('Is a Poset?', p_ds.isPoset())

    print('Reflective?', reflective)
    print('Antisimetric?', antisimetric)
    print('Transitive?', transitive)

    print('Is a Lattice?', l_ds.isLattice())
    print('Meet Irreducible', l_ds.meet_irreducible())
    print('Join Irreducible', l_ds.join_irreducible())
    print('Complement', l_ds.complement())


if __name__ == '__main__':
    main()
