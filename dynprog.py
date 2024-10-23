from itertools import combinations

class Task:
    def __init__(self, tproc=[], tddl=[]):
        self.njobs = len(tproc)
        if len(tddl) != self.njobs:
            raise IndexError("Excessive or not matching job numbers")
        self.tproc = tproc
        self.tddl = tddl

    def _tardy(self, tcomp, nddl):
        return max(tcomp-self.tddl[nddl], 0)

    def allcomb_search(self):
        jid = tuple(range(self.njobs))
        mem = {}
        for sz in range(1, self.njobs+1):
            for comb in combinations(jid, sz):
                tp = sum([self.tproc[i] for i in comb])
                tmin, imin = 0, []
                if len(comb) == 1:
                    imin = comb[0]
                    tmin = self._tardy(tp, comb[0])
                else:
                    for i in range(len(comb)):
                        tdi = self._tardy(tp, comb[i])
                        pcomb = comb[:i]+comb[i+1:]
                        prev = mem[pcomb][1]
                        tcomb = tdi + prev
                        if not tmin or tcomb < tmin:
                            imin = comb[i]
                            tmin = tcomb
                mem[comb] = (imin, tmin)
        tmin = mem[jid][1]
        traj = []
        cur = jid
        while len(cur) > 0:
            imin = mem[cur][0]
            traj.insert(0, imin+1)
            cur = tuple([i for i in cur if i != imin])
        return traj, tmin
    
    def tree_limsearch(self):
        tree = [([],0)]
        jid = range(self.njobs)
        tcomp = sum(self.tproc)
        result = []
        def insert_min(ite:list, child, tlim):
            add_node = False
            for t in range(len(ite)):
                if ite[t][1] > tlim:
                    ite.insert(t, (child, tlim))
                    add_node = True
                    break
            if not add_node:
                ite.append((child, tlim))
        while tree:
            node = tree.pop(0)
            for i in jid:
                if i not in node[0]:
                    child = node[0]+[i]
                    tprem = tcomp
                    tlim = 0
                    for c in child:
                        tlim += self._tardy(tprem, c)
                        tprem -= self.tproc[c]
                    if len(child) == self.njobs:
                        print(child)
                        if tlim <= tree[0][1]:
                            return ([c+1 for c in child[::-1]], tlim)
                        insert_min(result, child, tlim)
                    else:
                        insert_min(tree, child, tlim)
        return ([c+1 for c in result[0][::-1]], tlim)
                    
if __name__ == "__main__":
    t = Task([4,3,7,2,2]*4, [5,6,8,8,17]*4)
    # print(t.tree_limsearch())
    # t = Task([5,6,9,8,7]*3, range(9, 69, 4))
    # print(t.allcomb_search())
    print({1:0}.items())

