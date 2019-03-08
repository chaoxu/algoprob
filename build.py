import yaml
import re
import mistune
import functools
from jinja2 import Template, Environment, BaseLoader, FileSystemLoader
import os
import cgi
import sys
import networkx as nx
import string
from random import *
from operator import itemgetter

mk = mistune.Markdown(parse_block_html=True)

def is_str(x):
    # Python 3: isinstance(arg, str)
    return isinstance(x, basestring)
def remove_empty_lines(s):
    return '\n'.join(filter(lambda x: not re.match(r'^\s*$', x), s.splitlines()))
def compose(*functions):
    return functools.reduce(lambda f, g: lambda x: f(g(x)), functions, lambda x: x)

def set_default(y,x,default):
    if x not in y.keys() or y[x] is None:
        y[x] = default

def mki(x): 
    return mk(x)[3:-5]

def build_math(x):
    return '<span class="math">'+cgi.escape(x)+'</span>'
def my_replace(match):
    return build_math(match.group(1))

def yaml_loader(filepath):
    """Load a yaml file."""
    f = open(filepath, "r")
    s = f.read()
    data = yaml.load_all(s)
    return data

def math(string):
    # find $$ $$ pairs
    # return re.sub(r'\$\$(.*?)\$\$', r'<span class="math display">\1</span>', string)
    # find $ $ pairs
    return re.sub(r'\$(.*?)\$', my_replace, string)

def tohtml(string):
    z = compose(mki,math)
    return z(string)

def randomId():
    return "".join(choice(string.ascii_letters) for x in range(8))

def build_problems(problems):
    # problem statement
    # minimum required is problem, which defines the formal problem
    # everything else is optional
    # exercise are things one can say about the problem
    # optional title
    # tag: just list of tags that might make sense
    # notes are just everything else
    agg = []
    id_to_title = {}
    parents = {}
    p = {}

    # create the graph of problems
    D = nx.DiGraph()
    for problem in problems:
        set_default(problem,"inherit",[])
        set_default(problem,"parameters",[])
        set_default(problem,"algorithms",[])
        set_default(problem,"id",randomId())
        set_default(problem,"name","")

        p[problem["id"]] = problem
        for x in problem["inherit"]:
            D.add_edge(x,problem["id"])
    if not nx.is_directed_acyclic_graph(D):
        print "Not DAG"
    ordered = list(nx.topological_sort(D))

    index = {}
    for i in range(len(ordered)):
        index[ordered[i]] = i

    # we only inherit algorithm and parameters for now
    for problem in problems:
        v = problem["id"]
        if v in index:
            i = index[v]
        else:
            i = -1
        # p[v]["algorithms"] = [  (x,i)  for x in p[v]["algorithms"]]
        # for now we don't track how algorithm is inherited
        p[v]["parameters"] = [  (x,i)  for x in p[v]["parameters"]]

    # print p
    for v in ordered:
        for x in D.predecessors(v):
            # Inherit!
            parent = p[x]
            self   = p[v]
            self["parameters"] = mergeParameters(self["parameters"],parent["parameters"])
            self["algorithms"].extend(parent["algorithms"])
            self["algorithms"] = list(set(self["algorithms"]))
            if "description" not in self:
                if "description" in parent:
                    self["description"] = parent["description"]
    for v in ordered:
        zz = []
        for (t,i) in p[v]["parameters"]:
            if t["description"] is not None:
                zz.append((t,i))
        p[v]["parameters"] = zz
    return list(p.values())
    # inherit through topological sort order
    # create inherited problems    

def mergeParameters(A,B):
    # Larger number item does the replacement
    C = sorted(A+B, key=itemgetter(1))
    uni = {}

    for (x,i) in C:
        key = ""
        if "id" in x:
            key = x["id"]
        elif "type" in x and "name" in x:
            key = x["type"] + x["name"]
        uni[key] = (x,i)
    return list(uni.values())


def build_subroutine(subroutine):
    return subroutine

def build_presentation_complexity(complexity):
    presentation_complexity = {}
    presentation_complexity["name"] = complexity["name"]
    presentation_complexity["description"] = tohtml(complexity["description"])
    return presentation_complexity

def build_algorithms(algorithm):
    a = {}
    for x in algorithms:
        a[x["id"]] = x
    return a

def build_presentation_algorithm(algo):
    presentation_algo = {}
    presentation_algo["description"] = tohtml(algo["description"])
    presentaiton_subroutines = []
    if "subroutine" in algo:
        for x in algo["subroutine"]:
            y = build_subroutine(x)
            presentaiton_subroutines.append(y)
    presentation_algo["subroutine"] = presentaiton_subroutines

    presentation_algo["complexity"] = []
    for x in algo["complexity"]:
        presentation_algo["complexity"].append(build_presentation_complexity(x))

    return presentation_algo

def get_default(a,b,default):
    if b in a:
        return a[b]
    return default

def build_presentation(problems, algorithms):
    p = {}
    D = nx.DiGraph()
    presentation = {}
    # print problems
    for problem in problems:
        p[problem["id"]] = problem
        D.add_node(problem["id"])
        for x in problem["inherit"]:
            D.add_edge(x,problem["id"])

    glob = {}
    glob["id_to_title"] = {}


    for problem in problems:
        i = problem["id"]
        presentation[i] = {}
        presentation[i]["children"] = list(D.successors(i))
        presentation[i]["parents"]  = list(D.predecessors(i))
        presentation[i]["title"]    = tohtml(problem["name"])
        presentation[i]["description"] = tohtml(get_default(problem,"description",""))
        glob["id_to_title"][i] = presentation[i]["title"]
        presentation[i]["note"] = tohtml(get_default(problem,"note",""))
        # group parameters
        parameters= {}
        # print problem["parameters"]
        for (x,j) in problem["parameters"]:
            if x["type"] not in parameters:
                parameters[x["type"]] = []
            y = {}
            y["name"] = tohtml("$"+x["name"]+"$")
            if "description" in y:
                y["description"] = tohtml(x["description"])
            else:
                y["description"] = y["name"]
            parameters[x["type"]].append(y)
            # TODO, if we want to present inherit property, need to update with (y,j)
        presentation[i]["parameters"] = parameters

        presentation[i]["algorithms"] = []
        for algo in problem["algorithms"]:
            presentation[i]["algorithms"].append(build_presentation_algorithm(algorithms[algo]))
        
    return presentation, glob


    # problem_presentation

    # link all problems, add parents and children

def build_glossary(glossary):
    #print list(glossary)
    words = sorted(list(glossary.keys()))
    z = []
    for word in words:
        y = {}
        y["name"] = mki(math(word))
        y["definition"]=mki(math(glossary[word]))
        z.append(y)
    return z



env = Environment(loader=FileSystemLoader(""))
# build problems
problems = list(yaml_loader("problems.yaml"))
algorithms = list(yaml_loader("algorithms.yaml"))

parsed, glob = build_presentation(build_problems(problems),build_algorithms(algorithms))


glob["csstime"] = int(os.path.getmtime("default.css"))
# production or test
glob["production"] = (len(sys.argv) > 1)
template = env.get_template('problems.html')
with open('_site/index.html', 'w') as file:
    file.write(remove_empty_lines(template.render(problems=parsed, env=glob)).encode( "utf-8" ))

# build glossary
glossary = list(yaml_loader("glossary.yaml"))[0]
parsed = build_glossary(glossary)
template = env.get_template('glossary.html')
with open('_site/glossary.html', 'w') as file:
    file.write(remove_empty_lines(template.render(glossary=parsed, env=glob)).encode( "utf-8" ))
