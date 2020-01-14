import json
import re
import pprint as pp
import textwrap as tw
import nltk
from nltk.stem import WordNetLemmatizer
from keras.preprocessing.text import Tokenizer

text_dump = ''

with open("k_punk.json", "r") as read_file:
    data = json.load(read_file)
    for d in data:
        bit = ['\n'.join(t) for key, t in d.items() if key == 'text']
        text_dump = text_dump + '\n'.join(bit)
        text_dump = text_dump.encode('ascii','ignore').decode()
# print(text_dump)
wrapped = '\n'.join(tw.wrap(text_dump))
pp.pprint(wrapped)

write_file = open('k_punk.txt', 'w+')
write_file.write(wrapped)


initials = [('M', 'V')]...

with open("Conv1", "r") as read_file:
    data = load
    for d in data:

Newline
Collect interviewee/r's names
Newline

While not end
    if [before :] in interviewee_names:
        if not [laugh]
            remove things between () and []
            append to text base with [SPACE] tags in between


wrap
write to file
