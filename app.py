from flask import Flask, request, render_template
from dynprog import Task

app = Flask(__name__)

class Website:
    def __init__(self):
        self.njobs = 5
        self.jseq, self.tmap, self.metrics = [],[],{}
        self.mvi = -1
        self.table = []

    def stats(self):
        if self.mvi < 0:
            tcomp = 0
            table = []
            stat = ["Completion"]
            for jt in self.jseq:
                tcomp += site.tmap[0][jt[0]+1][1]
                stat.append(tcomp)
            table.append(stat)
            if "wt" in self.metrics:
                m = self.metrics["wt"]
                wsc = ["Weight compl."]
                ws = ["Weight"]
                for jt in self.jseq:
                    ws.append(self.tmap[m][jt[0]+1][1])
                    wsc.append(stat[jt[0]+1] * ws[-1])
                wsc.append(sum(wsc[1:]))
                table += [ws+["N/a"], wsc]
                stat.append("N/a")
            else:
                stat.append(sum(stat[1:]))
            if "dl" in self.metrics:
                m = self.metrics["dl"]
                tardy = ["Tardiness"]
                for jt in self.jseq:
                    tardy.append(max(0, stat[jt[0]+1] - self.tmap[m][jt[0]+1][1]))
                tardy.append(sum(tardy[1:]))
                table.append(tardy)

            self.table = table

site = Website()
task = Task()

@app.route('/', methods=['GET', 'POST'])
def index():
    fm = request.form
    print(fm)
    if fm.get("task"):
        site.njobs = int(fm.get("njobs"))
        site.tmap = [[("Processing time", "pr", 1,999,1)]+[[i, 5+i%3] for i in range(site.njobs)]]
        site.metrics["pr"] = len(site.metrics)
        if fm.get("weight"):
            site.tmap.append([("Weight", "wt", 0, 999, 0.01)] + [[i, 1+i%2] for i in range(site.njobs)])
            site.metrics["wt"] = len(site.metrics)
        if fm.get("deadline"):
            site.tmap.append([("Deadline", "dl", 1,999,1)] + [[i, 8+3*i] for i in range(site.njobs)])
            site.metrics["dl"] = len(site.metrics)
        site.jseq = []
    elif fm.get("tproc"):
        for row in site.tmap:
            for i in range(site.njobs):
                t = int(fm.get(f"{row[0][1]}_{i}"))
                row[i+1][1] = t
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
