import re
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import glob
from pathlib import Path


def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()


def write_new_file(list_of_lines, name):
    suf_res = [sub + "\n" for sub in list_of_lines]
    text_file = open(f'../data/{name}_NEW.Raw', "w")
    text_file.writelines(suf_res)
    text_file.close()


def clean_file(name, filename, quiet=True):
    a_file = open(name, "r")
    list_of_lines = a_file.readlines()

    # if the line is 25 char long, remove (no value, empty line with just the timestamp)
    list_of_lines = [line for line in list_of_lines if len(line) > 26]

    # combine the lines where the numbers for t2 was cut off onto a new line
    result_str = re.sub(r"\n[\d\/]+\,[\d/:]+\.\d{3}\,\ *(?=[\.\d\=])", "", ''.join(list_of_lines))
    list_of_lines = result_str.split('\n')

    results = [re.sub(r"\ *[A-Za-z]*\d*\=\ *", "", line) for line in list_of_lines]
    results = [re.sub(r"\ ", "", line) for line in results]

    if not quiet:
        print("Cleaned up!")
        print(f'length of  OG file: {len(list_of_lines)} \nlength of NEW lines: {len(results)}')

    write_new_file(results, filename)
    a_file.close()


if __name__ == '__main__':

    globs = glob.glob("../data/old/SBE45-TSG-MSG_*.Raw")
    for x in range(len(globs)):
        # Update Progress Bar
        print_progress_bar(x + 1, len(globs), prefix='Progress:', suffix='Complete', length=50)
        clean_file(globs[x], Path(globs[x]).stem)
