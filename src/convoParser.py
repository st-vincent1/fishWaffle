import os
import re
import textwrap as tw

def filters(s):
    # Interview comments
    if s.startswith("TIME") or s.startswith("INTERVIEW"):
        return False
    # Interview comments
    if s.startswith("NB"):
        return False
    # Short utterances can only be interruptions
    if len(s.split()) <= 2:
        return False
    # Empty utterances
    if re.findall(r'^\s*$', s):
        return False
    if not s:
        return False
    return True

def parse(s):
    start = False
    s = re.sub(r'\[anon\]', '**anon**', s)
    s = re.sub(r'\(([^()]+)\)|\[([^\[\]]+)\]', '', s)
    if re.findall(r'^[A-Z]+:', s):
        s = s[2:] if s[1] == ':' else s[3:]
        start = True
    s = re.sub(r'\s{2,}', ' ', s)
    return s.strip(), start



rel_path = re.sub(r'[^/]+$', '', os.getcwd())
conv_path = os.path.join(rel_path, 'data/convData')
train_path = os.path.join(rel_path, 'data/trainData')
if not os.path.isdir(train_path):
    os.mkdir(train_path)
for process_file in os.listdir(conv_path):
    f = open(os.path.join(conv_path, process_file))
    # dest_file_path = "conv" + str(i)
    line = f.readline()
    dump = ''
    speakers = []
    while(line == '\n'):
        line = f.readline()
    while(line != '\n'):
        speakers += [re.findall(r'[A-Z]+:', line)[0][:-1]]
        line = f.readline()
    while(line):
        s, start = parse(line)
        if filters(s):
            """
            between two sentences: put EOS tag if last character is a letter. Leave this otherwise.
            """
            if start:
                # If starting now, then previous has finished; finish previous sentence
                # If prev had a punctuation mark at the end, leave it there. Else, mark EOS
                if dump[:-1] not in '-,.?!':
                    dump += ' EOS '
                else:
                    dump += ' '
                # Append new utterance to dataset
                dump = dump + s
            else:
                dump = dump + ' ' + s
        line = f.readline()
    wrapped = '\n'.join(tw.wrap(dump))
    dest_file_path = "conv_" + '_'.join(speakers)
    write_text_file = open(os.path.join(train_path, dest_file_path), "w")
    write_text_file.write(wrapped)
    write_text_file.close()
