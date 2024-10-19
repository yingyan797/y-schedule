from flask import Flask, request, render_template
from dynprog import Task

app = Flask(__name__)

class Website:
    def __init__(self):
        self.njobs = 5
        self.jseq = []
        self.tmap = {}
        self.mvi = -1
        self.table = []

    def stats(self):
        if self.mvi < 0:
            tcomp = 0
            table = [["Completion"]]
            for jt in self.jseq:
                tcomp += self.tmap[jt[0]]
                table[0].append(tcomp)
            self.table = table

site = Website()
task = Task()

@app.route('/', methods=['GET', 'POST'])
def index():
    fm = request.form
    print(fm)
    if fm.get("task"):
        site.njobs = int(fm.get("njobs"))
        site.tmap = {i: 5 for i in range(site.njobs)}
        site.jseq = []
    elif fm.get("tproc"):
        for i in site.tmap.keys():
            t = int(fm.get(f"jt_{i}"))
            site.tmap[i] = t
        if not site.jseq:
            site.jseq = [[i, False] for i in range(site.njobs)]
        site.stats()
            
    elif site.jseq:
        if i:=fm.get("move"):
            mvi = int(i)
            if site.mvi < 0:
                site.mvi = mvi
                site.jseq[mvi][1] = True
            else:
                prev = site.jseq.pop(site.mvi)
                prev[1] = False
                site.jseq.insert(mvi, prev)
                site.mvi = -1
            site.stats()

    return render_template("index.html", site=site, jseq=[(i,site.jseq[i]) for i in range(len(site.jseq))])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
