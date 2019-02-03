import yaml
import re
import mistune
import functools
from jinja2 import Template, Environment, BaseLoader, FileSystemLoader
mk = mistune.Markdown(parse_block_html=True)
def compose(*functions):
    return functools.reduce(lambda f, g: lambda x: f(g(x)), functions, lambda x: x)

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

def build_problem(problem):
    parse = compose(mki,math)
    # problem statement
    # minimum required is problem, which defines the formal problem
    # everything else is optional
    # exercise are things one can say about the problem
    # optional title
    # tag: just list of tags that might make sense
    # notes are just everything else

    if "title" not in problem.keys() or problem["title"] is None:
        problem["title"] = ""
    if "tag" not in problem.keys() or problem["tag"] is None:
        problem["tag"] = []
    if "note" not in problem.keys() or problem["note"] is None:
        problem["note"] = ""
    if "problem" not in problem.keys() or problem["problem"] is None:
        problem["problem"] = ""
    if "exercise" not in problem.keys() or problem["exercise"] is None:
        problem["exercise"] = []
    if "opt" not in problem.keys() or problem["opt"] is None:
        problem["opt"] = []

    if isinstance(problem["opt"], basestring): # Python 3: isinstance(arg, str)
        problem["opt"] = [problem["opt"]]
    if isinstance(problem["tag"], basestring): # Python 3: isinstance(arg, str)
        problem["tag"] = [x.strip() for x in problem["tag"].split(',')]

    problem["title"] = parse(problem["title"])
    problem["tag"] = map(parse,problem["tag"])
    problem["note"] = parse(problem["note"])
    problem["problem"] = parse(problem["problem"])
    problem["exercise"] = map(parse,problem["exercise"])
    problem["opt"] = map(parse,problem["opt"])

    return problem 

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
parsed = map(build_problem,problems)
template = env.get_template('problems.html')
with open('_site/index.html', 'w') as file:
    file.write(template.render(problems=parsed).encode( "utf-8" ))

# build glossary
glossary = list(yaml_loader("glossary.yaml"))[0]
parsed = build_glossary(glossary)
template = env.get_template('glossary.html')
with open('_site/glossary.html', 'w') as file:
    file.write(template.render(glossary=parsed).encode( "utf-8" ))
