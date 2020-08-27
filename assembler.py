import json
import argparse
from hackparser import HackParser

def set_dest_bits(dest_string):
    """Recieves destination string from Instruction and returns the binary destination bits"""
    LETTERS = 'ADM'
    dest_bits = ['0','0','0']

    for letter in LETTERS:
                    if letter in dest_string.strip():
                        dest_bits[LETTERS.index(letter)] = '1'
    return ''.join(dest_bits)

def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("filename")
    args = arg_parser.parse_args()

    hack_parser = HackParser("pred_symbol_table.json")

    file_name = args.filename
    assembled_string = ''

    with open("syntax_table.json") as json_object:
        SYNTAX_SYMBOLS = json.load(json_object)

    with open(file_name) as file_object:
        line_list = hack_parser.parse(file_object)

    for line in line_list:
        if line[0] == '@':
            # Converts string after '@' to 16 bit binary number and appends. 
            assembled_string += f"{int(line[1:]):0>16b}" + '\n'
        else:
            if '=' in line and ';' in line:
                dest_string, comp_string = line.split('=') #ValueError exception if more than one '='
                comp_string, jmp_string = comp_string.split(';') #ValueError if more than one ';' after '='
                
                dest_bits = set_dest_bits(dest_string)
                comp_bits = SYNTAX_SYMBOLS[comp_string.strip()] #Error if incorrect comp syntax
                jmp_bits = SYNTAX_SYMBOLS[jmp_string.strip()] #Error if incorrect jmp syntax

                assembled_string += '111' + comp_bits + dest_bits + jmp_bits + '\n'
            elif '=' in line:
                dest_string, comp_string = line.split('=') #ValueError exception if more than one '='

                dest_bits = set_dest_bits(dest_string)
                comp_bits = SYNTAX_SYMBOLS[comp_string.strip()] #Error if incorrect comp syntax

                assembled_string += '111' + comp_bits + ''.join(dest_bits) + '000' + '\n'
            elif ';' in line:
                comp_string, jmp_string = line.split(';') #ValueError if more than one ';' after '='

                dest_bits = '000'
                comp_bits = SYNTAX_SYMBOLS[comp_string.strip()] #Error if incorrect comp syntax
                jmp_bits = SYNTAX_SYMBOLS[jmp_string.strip()] #Error if incorrect jmp syntax

                assembled_string += '111' + comp_bits + dest_bits + jmp_bits + '\n'
            else:
                print("Warning: Unused Computation")

    with open(file_name.split('.')[0] + ".hack", 'w') as file_object:
            file_object.write(assembled_string.strip())

if __name__ == "__main__":
    main()