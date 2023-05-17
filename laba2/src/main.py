import re
import argparse
import os

def init_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file-name', dest='file_name', required=True)
    parser.add_argument('--pattern', dest='pattern', required=True)
    return parser

def verify_cmd_args(file_name, pattern):
    if file_name == "":
        error = "file name is empty"
        print(error)
        raise Exception(error)
    else:
        print(f"File name is: {file_name}")
        print(f"Pattern is: {pattern}")

def creat_output_file_name(file_name, pattern):
    rest_of_file_name = '-'.join(file_name.split('-')[1:])
    output_file_name = f"{pattern}-{rest_of_file_name}"
    return output_file_name

def find_pattern_in_file(file_name, pattern):

    if not os.path.exists(file_name):
        error = f"File : {file_name} does not exist."
        print(error)
        raise Exception(error)

    output_file_name = creat_output_file_name(file_name, pattern)
    command = f"grep -iE \"{pattern}\" {file_name} > {output_file_name}"
    print(f"Executing {command=}")
    os.system(command)
    print(f"Result was collected in {output_file_name}")


if __name__ == "__main__":
    cmd_line_parser = init_parser()
    args = cmd_line_parser.parse_args()
    try:
        verify_cmd_args(args.file_name, args.pattern)
    except Exception as e:
        print(e)
        exit(-1)
    find_pattern_in_file(file_name=args.file_name, pattern=args.pattern)



