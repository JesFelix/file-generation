import os
import random

from . import read_json_file

data_file = os.path.join(os.path.dirname(__file__), "resources", "data.json")
data = read_json_file(data_file)
famous_quotes = data["famous"]      # a 代表前面垫话，b代表后面垫话
before_quotes = data["before"]      # 在名人名言前面弄点废话
after_quotes = data["after"]        # 在名人名言后面弄点废话
bosh = data["bosh"]                 # 代表文章主要废话来源

default_topic = "学生会退会"
repetitiveness = 2

def shuffle_iterate(items):
    global repetitiveness
    pool = list(items) * repetitiveness
    while True:
        random.shuffle(pool)
        for item in pool:
            yield item


next_bosh_sentence = shuffle_iterate(bosh)
next_famous_quote = shuffle_iterate(famous_quotes)


def get_famous_quote():
    global next_famous_quote
    sentence = next(next_famous_quote)
    sentence = sentence.replace("a", random.choice(before_quotes))
    sentence = sentence.replace("b", random.choice(after_quotes))
    return sentence


def new_paragraph():
    text = ". "
    text += "\r\n"
    text += "    "
    return text


def article_generation() -> str:
    topic = "狗屁不通"
    for _ in topic:
        tmp = str()
        while len(tmp) < 6000:
            branch = random.randint(0, 100)
            if branch < 5:
                tmp += new_paragraph()
            elif branch < 20:
                tmp += get_famous_quote()
            else:
                tmp += next(next_bosh_sentence)
        tmp = tmp.replace("x", topic)
        return tmp
