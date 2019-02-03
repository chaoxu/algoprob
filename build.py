import yaml
import re
import mistune
import functools
from jinja2 import Template

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

    if "title" not in problem.keys():
        problem["title"] = ""
    if "tag" not in problem.keys():
        problem["tag"] = []
    if "note" not in problem.keys():
        problem["note"] = ""
    if "problem" not in problem.keys():
        problem["problem"] = ""
    if "exercise" not in problem.keys():
        problem["exercise"] = []

    problem["title"] = parse(problem["title"])
    problem["tag"] = map(parse,problem["tag"])
    problem["note"] = parse(problem["note"])
    problem["problem"] = parse(problem["problem"])
    problem["exercise"] = map(parse,problem["exercise"])

    return problem 

def build_problems(problems):
    return map(build_problem,problems)

problems = list(yaml_loader("problems.yaml"))
# problems = list(yaml_loader("test.yaml")) 
parsed = map(build_problem,problems)

# print(parsed)
file = open("template.html", "r") 
template = Template(file.read())

print(template.render(problems=parsed).encode( "utf-8" ))
