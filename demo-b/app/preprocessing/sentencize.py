import math
from multiprocessing import Pool
import nltk


def scrub_line(line, min_sent_len=0, min_token_length=4):
    """
    Removes degenerate sentences that are less than 4 tokens long (including whitespace lines)
    splits a line into multiple sentences if there is more than one sentence on the input line
    line: str
    returns: str
    """
    scrubbed = "{}\n".format("\n".join(
        filter(
            lambda x: len([token for token in nltk.word_tokenize(x) if len(token) >= min_token_length]) > min_sent_len,
            nltk.sent_tokenize(line),
        )
    ))
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
    with in_path.open() as f_in:
        # open file to write out, creating it if it doesn't exist
        with out_path.open("w") as f_out:
            with Pool(workers) as p:
                for s_res in p.imap(scrub_line, f_in, chunksize=math.ceil(num_lines/workers)):
                    line_counter+=1
                    print(f'scrubbing: {(line_counter/num_lines)*100:.2f}%', flush=True)
                    if stripped:=s_res.strip():
                        f_out.write(stripped)