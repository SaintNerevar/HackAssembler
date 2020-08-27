""" Parser module for Hack Assembly Language """
import re
import json

class HackParser:
    """Class to parse .asm files written in Hack assembly language"""

    def __init__(self, symtable_json_filename):
        with open(symtable_json_filename) as json_object:
            self.symbol_table = json.load(json_object)

    def parse(self, file_object):
        """Parses the recieved file object and returns a list of parsed lines"""
        current_line = 0  
        next_address_available = 16  # Represents next address available for user defined variables.

        line_list = file_object.readlines()
        parsed_list = []

        # First Pass to remove whitespace and comments, and add Labels to symbol table.
        for line in line_list:
            # Removes comments with Regex check and strips off all whitespace. 
            parsed_line = ''.join(re.sub("//.*", '', line).strip().split())

            if parsed_line:
                if parsed_line[0] == '(':
                    # Add Labels to symbol table. Don't increment line number.
                    self.symbol_table[parsed_line[1:-1]] = str(current_line) 
                else:
                    current_line += 1
                    parsed_list.append(parsed_line)

        # Second Pass to replace labels and variables with respective numbers.
        for i in range(len(parsed_list)):
            first_char = parsed_list[i][0] # First char of Instruction
            a_string = parsed_list[i][1:]  # String after first character of Instruction

            if first_char == '@' and a_string in self.symbol_table:
                parsed_list[i] = '@' + self.symbol_table[a_string]
            # Condition checks if it's in fact a variable or a numeric address. 
            elif first_char == '@' and not a_string.isnumeric():
                self.symbol_table[a_string] = str(next_address_available)
                parsed_list[i] = '@' + str(next_address_available)
                next_address_available += 1

        return parsed_list