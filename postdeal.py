
import sys
sys.path.append('..')

import os
import re
import json
import codecs
import random
import numpy as np
from tqdm import tqdm
import datetime, time
import collections
from collections import Counter
from collections import defaultdict



ave = lambda x : sum(x)/len(x)
codecs_out = lambda x : codecs.open(x, 'w', 'utf-8')
codecs_in = lambda x : codecs.open(x, 'r', 'utf-8')

json_load = lambda x : json.load(codecs.open(x, 'r', 'utf-8'))
json_dump = lambda d, p: json.dump(d, codecs.open(p, 'w', 'utf-8'), indent=2, ensure_ascii=False)
json_dumps = lambda d: json.dumps(d, indent=2, ensure_ascii=False)

def json_dumpl(d, p) :
    output = codecs_out(p)
    for dt in d :
        output.write(json.dumps(dt, ensure_ascii=False)+'\n')
    output.flush()


config = json_load('config.json')

# =======   =======   =======   =======   =======   =======  

color = {
        # 'red'    : '#820010', # 听说这是北大红
        'blue'   : '#0066bb', 
        'red'    : '#FF0000', 
        'ignore' : '#FFFFFF',
        'black'  : '#000000',
        'lowest_weight' : '#EEEEEE',
        'lower_weight'  : '#999999',
    }

author2color = {}
for color_t, alist in config['author_highlight'] :
    if color_t in color :
        color_t = color[color_t]
    for at in alist :
        author2color[at] = color_t

def check_ingore(itemt) :
    # ignore_subj = ["Sound (cs.SD)", "Audio and Speech Processing (eess.AS)"]
    # ignore_desp = ["INTERSPEECH"]
    ignore_subj = config['ignore_subj']
    ignore_desp = config['ignore_desp']

    if any(t in itemt['subj'] for t in ignore_subj) :
        return True
    if any(t in itemt['desc'] for t in ignore_desp) :
        return True
    if any(t in itemt['jourref'] for t in ignore_desp) :
        return True
    return False

def deal_title(title) :
    for listt in config['title_highlight'] :
        if type(listt[1][0]) is list :
            break
        listt[1] += [t.lower() for t in listt[1]]
        listt[1] = [t.split() for t in listt[1]]
        listt[1] = sorted(listt[1], key=lambda x:len(x), reverse=True)

    to_ret = ''
    titlest = title.split()
    pt = 0
    while pt < len(titlest) :
        mark = False

        for color_t, phrase_list in config['title_highlight'] :
            if color_t in color :
                color_t = color[color_t]
            for igp in phrase_list :
                if ' '.join(titlest[pt:pt+len(igp)]).strip(':,!?') == ' '.join(igp) :
                    to_ret += '<font color="{}"> {}</font>'.format(color_t, ' '.join(igp))
                    pt += len(igp)
                    mark = True
                    break
            if mark : break
        
        if mark : continue
        to_ret += ' ' + titlest[pt]
        pt += 1
    return to_ret



def show(itemt, idt) :
    infor = {
        'idt'     : idt,
        'id'      : itemt['idt'],
        'title'   : deal_title(itemt['title']),
        'desc'    : itemt['desc'], 
        'jourref' : itemt['jourref'], 
        'subj0'   : itemt['subj'][0], 
        'subj1'   : '; '.join(itemt['subj'])[len(itemt['subj'][0]):], 
        'improtance' : color['black'],
    }

    if check_ingore(itemt) :
        infor['improtance'] = color['lowest_weight']
        infor['author'] = authort = ', \n                '.join(
            ['<a href="https://arxiv.org/search/cs?searchtype=author&query={}"><font color="{}">{}</font></a>'.format(t, color['lowest_weight'], t) for t in itemt['authors']])
    else :
        author_infor_list = []
        for t in itemt['authors'] :
            if not t in author2color:
                author_infor_list.append('<a href="https://arxiv.org/search/cs?searchtype=author&query={}">{}</a>'.format(t, t))
            else :
                author_infor_list.append('<a href="https://arxiv.org/search/cs?searchtype=author&query={}"><font color="{}">{}</font></a>'.format(t, author2color[t], t))
        infor['author'] = authort = ', \n                '.join(author_infor_list)
            

    to_ret = """
    <dt>
        <a name="item1">[{idt}]</a>
        &nbsp;  
        <span class="list-identifier">
            <a href="https://arxiv.org/abs/{id}" title="Abstract">arXiv:{id}</a>
             [
            <a href="https://arxiv.org/pdf/{id}" title="Download PDF">pdf</a>
            , 
            <a href="https://arxiv.org/ps/{id}" title="Download PostScript">ps</a>
            , 
            <a href="https://arxiv.org/format/{id}" title="Other formats">other</a>
            ]
        </span>
    </dt>
    <dd>
        <div class="meta">
            <div class="list-title mathjax">
                <span class="descriptor">Title:</span>
                 <font color="{improtance}">{title}</font>
            </div>
            <div class="list-authors">
                <span class="descriptor">Authors:</span>
                {author}
            </div>
            <div class="list-comments mathjax">
                <span class="descriptor">Comments:</span>
                 {desc}
            </div>
            <div class="list-journal-ref">
                <span class="descriptor">Journal-ref:</span>
                 {jourref}
            </div>
            <div class="list-subjects">
                <span class="descriptor">Subjects:</span>
                <span class="primary-subject">{subj0}</span>
                {subj1}
            </div>
        </div>
        <br>
    </dd>
    """.format(**infor)
    return to_ret

def generate_page(items, output_name) :
    mark_place = 'HEREISTHEPLACEFORTHECONTENTS'
    t_html = codecs_in('template.html').readlines()
    i_mark = [i for i in range(len(t_html)) if t_html[i].strip() == mark_place][0]

    t_html[i_mark] = ''
    for idt, itemt in enumerate(items) :
        t_html[i_mark] += show(itemt, idt)

    output = codecs_out(output_name)
    for line in t_html :
        output.write(line)
    output.flush()
    output.close()


if __name__ == '__main__':
    data = json_load(sys.argv[1])
    generate_page(data, sys.argv[2])

   

"""
python3 postdeal.py arxiv_20210529.json arxiv_20210529.html 
"""

