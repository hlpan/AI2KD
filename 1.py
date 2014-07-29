# coding=utf-8
from bs4 import BeautifulSoup


word_list = []
infl_list = []


def set_value_attribute():
    """
    修改源html文件
    给idx:orth 的 value属性赋值
    """
    Fobj = open("Xian Dai Ying Yi Ci Dian - Wei Zhi.html", "r",
                encoding="utf-8")
    data = Fobj.read()
    Fobj.close()
    soup = BeautifulSoup(data)

    # 先找出所有的idx:entry
    entrylist = soup.findAll("idx:entry")
    for entry in entrylist:
        # 单词
        the_word = entry.word.get_text()
        # 过滤，如把ABC1改成ABC，如果最后一个字符是数字，就去掉
        if the_word[-1] <= '9' and the_word[-1] >= '0':
            the_word = the_word[:-1]
        # 再做一次
        if the_word[-1] <= '9' and the_word[-1] >= '0':
            the_word = the_word[:-1]
        # 赋给value
        entry.find('idx:orth')['value'] = the_word

    Fobj = open('my.html', 'w', encoding="utf-8")
    Fobj.write(str(soup))
    Fobj.close()
    pass


def search_inflection(word):
    """
    查找一个word的变形
    """
    pass


def list_all_word():
    """
    处理字典value的同时，把所有单词列成一个list
    """
    global word_list
    Fobj = open("my.html", "r", encoding="utf-8")
    data = Fobj.read()
    Fobj.close()

    soup = BeautifulSoup(data)
    # 先找出所有的idx:entry
    entrylist = soup.findAll("idx:entry")
    for entry in entrylist:
        # 单词
        the_word = entry.word.get_text()
        # 过滤，如把ABC1改成ABC，如果最后一个字符是数字，就去掉
        if the_word[-1] <= '9' and the_word[-1] >= '0':
            the_word = the_word[:-1]
        # 再做一次
        if the_word[-1] <= '9' and the_word[-1] >= '0':
            the_word = the_word[:-1]
        # 赋给value
        entry.find('idx:orth')['value'] = the_word
        #print(the_word)
        word_list.append(the_word)


def split_infl_line(line):
    """
    处理infl_list文件中的一行
    infl_list中的种类如下：
    0.空
    1.“|”
    2.单词 (单词) (单词 单词)
    3.@单词 (@单词) (@单词 @单词)
    4.-单词 (-单词) (-单词 -单词)
    5.~单词 (~单词) (~单词 ~单词)

    {单词}这种不是，表示应用范围

    对于一个字符串，判断
    1.是空，删除
    2.是"|"，删除
    3.第一个字符是"("，删除字符；是"{"，删除字符串
        4.最后一个字符是")"，删除字符
    5.第一个字符是"@" "-" "~"，删除字符
    6.

    infl_list每一行中，第一个单词是原型，后面的每一个单词是变形
    对于infl_list文件中每一个单词，
    如果它的变形列表中的单词出在word_list中，
    那么在变形列表中删除它
    """

    global infl_list
    words_to_delete = []
    orig_and_inf = []
    # 冒号之前是原型
    line_cut = line.split(':')
    # 获得单词原型
    the_orignal_word = line_cut[0].split(' ')[0]

    orig_and_inf.append(the_orignal_word)

    # 冒号后面是变形列表
    infl_splited = line_cut[1].split(' ')
    for inflection in infl_splited:
        if len(inflection) >= 1 and inflection[-1] == '\n':
            # 删除最后一字符
            inflection = inflection[0:-1]
        if len(inflection) < 1 or inflection == '|' \
                or inflection[0] == '{':
            # 不处理
            continue
        if inflection[0] == '(':
            # 删除第一个字符
            inflection = inflection[1:]
        if inflection[-1] == ')':
            # 删除最后一字符
            inflection = inflection[0:-1]
        if inflection[0] == '-' or inflection[0] == '~' \
                or inflection[0] == '@':
            # 删除第一个字符
            inflection = inflection[1:]

        orig_and_inf.append(inflection)

    #去掉重复的
    f = open("words_to_delete.txt", "w",
             encoding="utf-8")
    for x in range(1, len(orig_and_inf)):
        if orig_and_inf[x] in word_list:
            words_to_delete.append(orig_and_inf[x])
    if len(words_to_delete) >= 1:
        f.write("删除的单词是%s" % (words_to_delete))
    for word_to_delete in words_to_delete:
        orig_and_inf.remove(word_to_delete)
    # 处理干净后，加入列表
    infl_list.append(orig_and_inf)
    f.close()


def trim_infletion():
    """
    处理infl_list文件
    对于word_list中的单词，如果它出现在infl_list文件变形列表中时，
    那么在变形列表中删除它。
    换句话说就是，对于infl_list文件中每一个单词，
    如果它的变形列表中的单词出在word_list中，
    那么在变形列表中删除它
    """
    file = open("2of12id.txt", "r", encoding="utf-8")

    global infl_list

    while 1:
        lines = file.readlines(100000)
        if not lines:
            break
        for line in lines:
            split_infl_line(line)

def main():
    """
    首先，列出所有单词表，到word_list文件
    然后，对于word_list中的单词，如果它出现在infl_list文件变形列表中时，
    那么在变形列表中删除它
    最后在dict.html文件中，对于每一个单词word,给它添加变形数据列表
    """
    #set_value_attribute()
    list_all_word()
    f = open("wordlist.txt", "w", encoding="utf-8")
    for word in word_list:
        f.write("%s\n" % (word))
    f.close()
    #trim_infletion()

if __name__ == '__main__':
    main()
