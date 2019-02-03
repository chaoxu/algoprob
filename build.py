import yaml
import re
import mistune
import functools
from jinja2 import Template, Environment, BaseLoader, FileSystemLoader
import os
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
    return re.sub(r'\$(.*?)\$', r'<span class="math">\1</span>', string)

def build_problems(problems):
    parse = compose(mki,math)
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
    for problem in problems:
        set_default(problem,"title","")
        set_default(problem,"tag",[])
        set_default(problem,"note","")
        set_default(problem,"problem","")
        set_default(problem,"exercises",[])
        #set_default(problem,"opt",[])
        set_default(problem,"algorithms",[])
        set_default(problem,"children",{})
        set_default(problem,"id","")

        #if is_str(problem["opt"]): 
        #    problem["opt"] = [problem["opt"]]
        if is_str(problem["tag"]):
            problem["tag"] = [x.strip() for x in problem["tag"].split(',')]

        problem["title"] = parse(problem["title"])
        problem["tag"] = map(parse,problem["tag"])
        problem["note"] = parse(problem["note"])
        problem["problem"] = parse(problem["problem"])
        problem["exercises"] = map(parse,problem["exercises"])

        #problem["opt"] = map(parse,problem["opt"])

        children = []
        for (key,value) in problem["children"].items():
            z={}
            z["id"] = key
            z["description"] = parse(value)
            if key not in parents.keys():
                parents[key] = set()
            parents[key].add(problem["id"]) 
            children.append(z)

        problem["children"] = children

        for algorithm in problem["algorithms"]:
            algorithm["description"] = parse(algorithm["description"])
            algorithm["complexity"] = parse(algorithm["complexity"])
            set_default(algorithm, "problem", [])
            if is_str(algorithm["problem"]):
                algorithm["problem"] = [algorithm["problem"]]
        agg.append(problem)
        id_to_title[problem["id"]] = problem["title"]

    # update children
    for problem in problems:
        if problem["id"] in parents.keys():
            problem["parents"] = list(parents[problem["id"]])
        else:
            problem["parents"] = []
    env={}
    env["id_to_title"] = id_to_title
    return agg, env

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
parsed, glob = build_problems(problems)

glob["csstime"] = int(os.path.getmtime("default.css"))
template = env.get_template('problems.html')
with open('_site/index.html', 'w') as file:
    file.write(remove_empty_lines(template.render(problems=parsed, env=glob)).encode( "utf-8" ))

# build glossary
glossary = list(yaml_loader("glossary.yaml"))[0]
parsed = build_glossary(glossary)
template = env.get_template('glossary.html')
with open('_site/glossary.html', 'w') as file:
    file.write(remove_empty_lines(template.render(glossary=parsed, env=glob)).encode( "utf-8" ))
