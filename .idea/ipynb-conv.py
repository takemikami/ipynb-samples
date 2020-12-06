#!/usr/bin/env python3

import json
import sys
import os

# ipynb -> ipynb-code
def ipynb2code(fipynb, fcode):
    with open(fipynb, 'r') as fjson:
        ipynb = json.load(fjson)

    src = []
    for cell in ipynb['cells']:
        cell_type = " md" if cell['cell_type'] == 'markdown' else ""
        src.append("#%%" + cell_type)
        src.append("")
        for ln in cell['source']:
            src.append(ln.rstrip())
        src.append("")

    with open(fcode, 'w') as f:
        for ln in src:
            f.write(ln)
            f.write("\n")


# ipynb-code -> ipynb
def code2ipynb(fipynb, fcode):
    with open(fcode, 'r') as fin:
        src = fin.read()

    lines = src.split('\n')
    cells = []
    cell = None
    source = []
    for ln in lines:
        if ln.startswith("#%%"):
            if cell is not None:
                source = source[1:-1]
                source[-1] = source[-1].rstrip()
                cell['source'] = source
                cells.append(cell)
            source = []
            cell = {}
            if ln.startswith("#%% md"):
                cell['cell_type'] = 'markdown'
                cell['metadata'] = {"collapsed": False, "pycharm": {"name": "#%% md\n"}}
            else:
                cell['cell_type'] = 'code'
                cell['outputs'] = []
                cell['execution_count'] = None
                cell['metadata'] = {"collapsed": True, "pycharm": {"name": "#%%\n"}}
        else:
            source.append(ln + "\n")
    if cell is not None:
        source = source[1:-1]
        source[-1] = source[-1].rstrip()
        cell['source'] = source
        cells.append(cell)

    with open(fipynb, 'w') as fjson:
        json.dump({
            'cells': cells,
            'metadata': {
                "kernelspec": {
                    "display_name": "Python 3",
                    "language": "python",
                    "name": "python3"
                },
                "language_info": {
                    "codemirror_mode": {
                        "name": "ipython",
                        "version": 2
                    },
                    "file_extension": ".py",
                    "mimetype": "text/x-python",
                    "name": "python",
                    "nbconvert_exporter": "python",
                    "pygments_lexer": "ipython2",
                    "version": "2.7.6"
                }
            },
            "nbformat": 4,
            "nbformat_minor": 0
        }, fjson, indent=2)

if len(sys.argv) > 1:
    fn_ipynb = sys.argv[1]
    fn_ipynb_code = ".ipynb-src/{}-code".format(fn_ipynb)
    reverse = False
    if len(sys.argv) > 2:
        subopt = sys.argv[2]
        if subopt == '-r':
            reverse = True
    os.makedirs('.ipynb-src', exist_ok=True)
    if reverse:
        code2ipynb(fn_ipynb, fn_ipynb_code)
    else:
        ipynb2code(fn_ipynb, fn_ipynb_code)
