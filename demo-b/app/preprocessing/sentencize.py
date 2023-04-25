import math
from multiprocessing import Pool
import nltk
from tqdm import tqdm
import re

def tokenize_words(text, min_length=0):
    r = re.compile("[a-zA-Z\.]+")
    r_html = re.compile("<.*?>")  # Match HTML tags
    r_acronym = re.compile("\.")

    text = r_html.sub("", text)
    text = r_acronym.sub("", text)
    tokens = r.findall(text)
    tokens = [t for t in tokens if len(t) >= min_length]

    return tokens

def scrub_line(line, min_sent_len=0, min_token_length=4):
    """
    Removes degenerate sentences that are less than 4 tokens long (including whitespace lines)
    splits a line into multiple sentences if there is more than one sentence on the input line
    line: str
    returns: str
    """
    # won't drop small words, just small sentences
    filtered_line = [" ".join(s) for s in filter(lambda x: len(x) > min_sent_len,
                                                 map(lambda x: [token for token in nltk.word_tokenize(x) if
                                                                len(token) >= min_token_length],
                                                     nltk.sent_tokenize(line)))]
    # filtered_line = [" ".join(s) for s in filter(lambda x: len(x) > min_sent_len,
    #                                              map(lambda x: tokenize_words(x, min_token_length),
    #                                                  nltk.sent_tokenize(line)))]
    scrubbed = "{}\n".format("\n".join(filtered_line))
    # scrubbed = "{}\n".format("\n".join(
    #     filter(
    #         lambda x: len([token for token in nltk.word_tokenize(x) if len(token) >= min_token_length]) > min_sent_len,
    #         nltk.sent_tokenize(line),
    #     )
    # ))
    return scrubbed


def initial_scrub(in_path, out_path, workers=48):
    """
    in_path: Path object to a plaintext_file
    out_path: Path object to the location we should write the scrubbed file
    reads the file and writes a file to out_path such that every line contains exactly one sentence as determined by nltk's sentence tokenizer
    uses streams and iterators so we don't load the entire file into memory at once
    will consume tons of memory if the whole file is on one line
    creates file at out_path if it doesn't exist
    """
    line_counter = 0
    with in_path.open() as f_in:
        num_lines = len(f_in.readlines())
    sentences=[]
    print('scrubbing file')
    with in_path.open() as f_in:
        # open file to write out, creating it if it doesn't exist
        with Pool(workers) as p:
            for s_res in tqdm(p.imap(scrub_line, f_in, chunksize=math.ceil(num_lines / workers))):
                line_counter += 1
                sentences.append(s_res)
    print('writing to file')
    with out_path.open("w") as f_out:
        f_out.writelines(sentences)
    print('wrote to file')
    return sentences
