import os
import re
import textwrap as tw

def filters(s):
    if s.startswith("TIME") or s.startswith("INTERVIEW"):
        return False
    if s.startswith("NB"):
        return False
    if re.findall(r'^\s*$', s):
        return False
    if not s:
        return False
    return True

def parse(s):
    start = False
    s = re.sub(r'\[inc\]', '**inc**', s)
    s = re.sub(r'\(([^()]+)\)|\[([^\[\]]+)\]', '', s)
    if s[0:2] in speakers:
        s = s[2:]
        start = True
    s = re.sub(r'\s{2,}', ' ', s)
    return s.strip(), start



rel_path = re.sub(r'[^/]+$', '', os.getcwd())
conv_path = os.path.join(rel_path, 'data/convData')
train_path = os.path.join(rel_path, 'data/trainData')
if not os.path.isdir(train_path):
    os.mkdir(train_path)
i = 0
for process_file in os.listdir(conv_path):
    f = open(os.path.join(conv_path, process_file))
    dest_file_path = "conv" + str(i)
    line = f.readline()
    dump = ''
    speakers = []
    while(line == '\n'):
        line = f.readline()
    while(line != '\n'):
        speakers += [line[0:2]]
        line = f.readline()
    while(line):
        s, start = parse(line)
        if filters(s):
            if start:
                dump = dump + '... ' + s
            else:
                dump = dump + ' ' + s
        line = f.readline()
    wrapped = '\n'.join(tw.wrap(dump[4:]))
    write_text_file = open(os.path.join(train_path, dest_file_path), "w+")
    write_text_file.write(wrapped)
    write_text_file.close()
    i += 1
