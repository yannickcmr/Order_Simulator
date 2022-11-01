import re, io, os, sys, codecs, time, linecache
import random as rnd

try:
    sys.stdin = codecs.getreader("utf-8")(sys.stdin.detach())
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
except:
    pass  


Path_Saving = "/Test/"

# Lists to calculate the hash.
letters_list = ["e", "i","a", "u" , "o", "n", "s", "r", "t", "d", "h", "l", "b", "c", "f", "g", "j", "k", "m", "p", "q", "v", "w", "x", "y", "z"]
prime_nums = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
nums = [str(i) for i in range(0, 10)]

# Lists of words to throw out i.e. words of connection, etc.
articles_list = ["der", "die", "das", "des", "dem", "den", "des", "ein", "eine", "einen", "eines", "einem", "einer"]
prepositions_list = ["von", "nach", "aus", "auf", "mit", "seit", "neben", "über", "unter", "vor", "vom", "bis", "durch", "für", "gegen"]
connectors_list = ["und", "auch", "nicht", "oder", "falls", "sowie"]

# remove unwanted words in product tags.
def reduce_tags(tag: str) -> list:
    # Discared all the unessential words and tags regarding the hash.
    tag = tag.lower()
    tags_list = tag.split(",")
    #print(tags_list)
    remove_tags = [*re.findall(r"\b(?:% s)\b" % "|".join(articles_list), tag)]
    remove_tags += re.findall(r"\b(?:% s)\b" % "|".join(prepositions_list), tag)
    remove_tags += re.findall(r"\b(?:% s)\b" % "|".join(connectors_list), tag) 
    remove_tags += re.findall(r"\b(\w|\W)\b", tag) # remove words of len = 1
    remove_tags += re.findall(r"\b(\w\w)\b", tag) # remove words of len = 2
    return [x for x in tags_list if x not in remove_tags]

def calc_hash_prime(word: str) -> int:
    # calc the number to use in the hash function. Is based on primes.
    word_list = list(word)
    index = [letters_list.index(x) for x in word_list]
    sum = 0
    if len(index) < 25:
        for i in range(0, len(index)):
            sum += prime_nums[i]**index[i]
        return sum
    else:
        print(f"word too long to hash: {word}")
        return 0

def calc_ten_sum(num: int) -> int:
    # just a way to keep the values somewhat reasonable. Adds them up to below 100.
    sum = 0
    for integer in list(str(num)):
        sum += int(integer)
    if sum > 99: sum = calc_ten_sum(sum)
    return sum

def get_line_in_doc(line: int, doc: str = "tags_compiled.csv"):
    # Find the corresponding line in the doc.
    doc = os.path.join(Path_Saving, doc)
    cache = linecache.getline(doc, int(line))
    return cache.translate({ord("\n"): None})

def check_tag(tag: str):
    # Search for tag in doc.
    line_num = calc_ten_sum(calc_hash_prime(tag))
    line = get_line_in_doc(line_num)
    if len(line) > 0:
        match_str = f"{tag}:"
        in_line = re.search(match_str, line)
        if in_line != None:
            span = in_line.span()[1]
            return line[span: span + 7]
    return None

def create_code(pocket: int) -> str:
    # Creates a random code for a tag.
    space_list = [*nums, *letters_list]
    code = [rnd.choice(space_list) for i in range(0, 5)]
    code = "".join(code)
    if pocket < 10: pocket = f"0{str(pocket)}"
    code = str(pocket) + code.upper()
    return code

def add_to_tags_list(tag:str, tag_comp: str, doc: str = "tags_compiled.csv") -> None:
    doc = os.path.join(Path_Saving, doc)
    with io.open(doc, "r", encoding="utf-8") as tags_doc:
        lines = tags_doc.readlines()

    index = int(tag_comp[:2]) -1
    lines[index] =  lines[index].translate({ord("\n"): None})
    lines[index] += f"{tag}:{tag_comp};\n"
    with io.open(doc, "w+", encoding="utf-8") as tags_doc:
        tags_doc.writelines(lines)

def get_prefix(tags: list) -> str:
    # Returns a str with the condensed prefixes.
    prefix = ""
    for tag in tags:
        prefix += f"{str(int(tag[0:2]))},"
    return prefix

def compile_tags(tags: str) -> list:
    # hashify the tags of a product
    comp_tags = []
    tags_ = reduce_tags(tags)
    for item in tags_:
        cache = check_tag(item)
        if cache == None:
            index = calc_ten_sum(calc_hash_prime(item))
            cache = create_code(index)
            add_to_tags_list(item, cache)
        comp_tags.append(cache)
    return ",".join(comp_tags), get_prefix(comp_tags)


if __name__ == "__main__":
    start = time.perf_counter()
    print("-----------------------------------")
    test_tags = ["Home,Vine,Decor,GOESWELL,LEDs,Decoration,Willow,Wall,White,Vineyard,Warm,Artificial",
                        "Spielfiguren,Thrones,der,of,Musik,mit,Game,den,Brettspiel",
                        "Das,und,Familienkreis,Freundes,Jung,Spieleabende,im,Kartenspiel,von,Magilano,Alt,unterhaltsame,ideale,Geschenk"]
    for item in test_tags:
        print(item)
        cache = compile_tags(item)
        print(cache)

    print(f"done in {time.perf_counter() - start} time.")
    