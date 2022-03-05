import argparse
from markdown_to_text import *

def rm_newlines(s):
    return s.replace("\n", " ")

def table_header(langs):
    return "| {} |\n| {} |".format(
                " | ".join(langs), 
                " | ".join(list(map(lambda _: "---", langs)))
    )
            
def table_row(table_dict, i):
    return "| {} |".format(
        " | ".join([table_dict[lang][i] for lang in table_dict.keys()])
    )

def table(langs, table_dict):
    return table_header(langs) + "\n" + "\n".join(
        [table_row(table_dict, i) for i in range(len(table_dict[langs[0]]))]
    )

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='''Turn paragraph-aligned plain text files into a markdown
                       table for parallel display''')
    parser.add_argument(
        'paths', 
        metavar='PATHS', 
        type=str,
        nargs='+', 
        help='paragraph-aligned text files')
    parser.add_argument(
        '--langs', 
        metavar='LANGUAGES', 
        type=str, 
        help='comma-separated list of languages to be used as table headers')
    
    args = parser.parse_args()
    paths = args.paths
    if args.langs:
        langs = args.langs.split(",")
    else:
        langs = list(map(str,range(1,len(paths) + 1)))
    if len(langs) != len(paths):
        print("The number of languages does not match the number of files")
        exit(1)
    table_dict = {}
    for (lang,path) in zip(langs,paths):
        with open(path) as f:
            content = f.read()
        table_dict[lang] = list(map(
            lambda p: markdown_to_text(rm_newlines(p)), content.split("\n\n"))
        )
    # TODO: check that the number of files is the same for all files
    print(table(langs, table_dict))

    