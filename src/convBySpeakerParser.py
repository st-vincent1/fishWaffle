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
    speaker = False
    s = re.sub(r'\[anon\]', '**anon**', s)
    s = re.sub(r'\(([^()]+)\)|\[([^\[\]]+)\]', '', s)
    if re.findall(r'^[A-Z]+:', s):
        speaker = s[0]
        s = s[2:] if s[1] == ':' else s[3:]
        start = True
    s = re.sub(r'\s{2,}', ' ', s)
    return s.strip(), start, speaker

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
    utterance_dict = {}
    while(line == '\n'):
        line = f.readline()
    while(line != '\n'):
        speakers += [re.findall(r'[A-Z]+:', line)[0][:-1]]
        line = f.readline()
    while(line):
        s, start, speaker = parse(line)
        if filters(s):
            if(speaker):
                current_speaker = speaker
            """
            between two sentences: put EOS tag if last character is a letter. Leave this otherwise.
            """
            if current_speaker not in utterance_dict:
                utterance_dict[current_speaker] = s
            else:
                if start:
                    # If starting now, then previous has finished; finish previous sentence
                    # If prev had a punctuation mark at the end, leave it there. Else, mark EOS
                    if utterance_dict[current_speaker].strip()[-1:] not in '-,.?!':
                        utterance_dict[current_speaker] += ' EOS '
                    else:
                        utterance_dict[current_speaker] += ' '
                    # Append new utterance to dataset
                    utterance_dict[current_speaker] = utterance_dict[current_speaker] + s
                else:
                    utterance_dict[current_speaker] = utterance_dict[current_speaker] + ' ' + s
        line = f.readline()
    for speaker in speakers:
        if speaker in utterance_dict:
            wrapped = '\n'.join(tw.wrap(utterance_dict[speaker]))
            dest_file_path = "conv_" + '_'.join(speakers) + '@Speaker_' + speaker
            write_text_file = open(os.path.join(train_path, dest_file_path), "w")
            write_text_file.write(wrapped)
            write_text_file.close()
