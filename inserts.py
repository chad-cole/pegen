import argparse
import pprint
import sys
import token
import tokenize
import traceback

from pegen.tokenizer import Tokenizer
from pegen.testutil import recovery_by_insertions, describe_token

from parse import GeneratedParser


# A variation of simple_parser_main() in pegen/parser.py.
def main() -> None:
    argparser = argparse.ArgumentParser()
    argparser.add_argument("filename", help="Input file ('-' to use stdin)")

    args = argparser.parse_args()

    filename = args.filename
    if filename == "" or filename == "-":
        filename = "<stdin>"
        file = sys.stdin
    else:
        file = open(args.filename)
    try:
        tokengen = tokenize.generate_tokens(file.readline)
        tokenizer = Tokenizer(tokengen)
        parser = GeneratedParser(tokenizer)
        tree = parser.file()
        if not tree:
            err = parser.make_syntax_error(filename)
            traceback.print_exception(err.__class__, err, None)
            got, farthest, expected, howfar = recovery_by_insertions(parser)
            if expected:
                print(
                    f"Got {describe_token(got, parser)}, expected one of the following:",
                    ", ".join(describe_token(tok, parser) for tok in expected),
                    f"[reached {farthest}]",
                )
            sys.exit(1)
    finally:
        if file is not sys.stdin:
            file.close()

    pprint.pprint(tree, indent=2)


if __name__ == "__main__":
    main()