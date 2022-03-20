import re
import random

class ControlFlowObfuscation:
    def __init__(self, filename):
        self.filename = filename

        # Read Smali file
        with open(self.filename, "r") as f:
            self.content = f.read()

        self.methods = self.get_methods()
            

    def get_methods(self):
        """
            Get all methods in the smali file and store them to a list

            Params:

            Returns:
                smali_method_list(List): List of smali method codes

        """
        # Get methods in Smali file using re
        pattern = "^\.method[\s\S]*?\.end\smethod"
        smali_method_list = re.findall(pattern, self.content, re.MULTILINE)

        return smali_method_list


    def split_method_by_line(self, method):
        """
            Splits the methods at every .line into smaller Smali code chunks

            Params:
                method(Str): Method to be split
            Returns:
                split_method_list(List): List of smaller smali method code chunks

        """
        temp_method_chunk_builder = ""
        split_method_list = []

        # Split method into single lines and append them to a string but break when .line is found
        split_method_lines = method.splitlines()
        function_declaration = split_method_lines[0]
        end_method = split_method_lines[-1]

        for line in split_method_lines[1:-1]:
            if line.startswith('    .line'):
                split_method_list.append(temp_method_chunk_builder)
                temp_method_chunk_builder = ""

            temp_method_chunk_builder += line + "\n"
        split_method_list.append(temp_method_chunk_builder)

        # Add back method declaration and end method
        split_method_list.insert(0, function_declaration)
        split_method_list.append(end_method)

        return split_method_list

    def get_locals_number(self, method):
        """
            Get the number of local registers

            Params:
                method(Str): Method to extract number of local registers from
            Returns:
                locals_number(Int): Current .locals number

        """
        locals_line = method.split("\n")[1]
        locals_number = locals_line.split()[1]
        return locals_number

    def add_pswitch_const_goto(self, chunk, pswitch, next_const, locals_number):
        """
            Add :obf_pswitch_0 | const vx, next_const | :goto obfus_loop to smali code

            Params:
                chunk(Str): Method for code to be added
                pswitch(Int): Switch number
                next_const(Int): Next switch case to jump to
                locals_number(Int): The register number

            Returns:
                chunk(Str): return code with added pswitch const and goto

        """
        lines = chunk.split("\n")
        string_builder_temp = f"    :obf_pswitch_{pswitch}\n"
        lines.insert(0, string_builder_temp)
        if next_const != -1:
            string_builder_temp = f"    const v{locals_number}, {next_const}"
            lines.insert(-1, string_builder_temp)
        string_builder_temp = "    :goto obfus_loop"
        lines.insert(-1, string_builder_temp)
        
        return "\n".join(lines)

    def get_imports(self):
        imports_list = []
        for item in self.content.split("\n"):
            if item.startswith(".method"):
                break
            imports_list.append(item)
        return "\n".join(imports_list)

    def method_obfuscator(self, method):
        LOCALS_CHUNK = 1
        LOCALS_LINE = 0
        FIRST_CHUNK = 3

        
        locals_number = int(self.get_locals_number(method))
        split_method_list = self.split_method_by_line(method)

        # Create new register to store value for switch case
        new_locals_number = locals_number + 1
        lines = split_method_list[LOCALS_CHUNK].split("\n")
        lines[LOCALS_LINE] = f"    .locals {new_locals_number}"
        split_method_list[LOCALS_CHUNK] = "\n".join(lines)

        # Initialize value of new register with 0, create packed switch
        string_builder_temp = f"    const v{locals_number}, 0\n"
        string_builder_temp += "    :obfus_loop\n"
        string_builder_temp += f"    packed-switch v{locals_number}, :pswitch_obf\n"
        split_method_list.insert(2, string_builder_temp)

        # Randomise the order of code chunks
        chunks_to_modify_list = split_method_list[4:-1]
        order_list = list(range(len(chunks_to_modify_list)))
        random.shuffle(order_list)

        if len(chunks_to_modify_list) == 0:
            # Create default case 0, first chunk code of split code
            split_method_list[FIRST_CHUNK] = self.add_pswitch_const_goto(split_method_list[FIRST_CHUNK], 0, -1, locals_number)
            # Create Switch table at the end
            string_builder_temp = "    :pswitch_obf\n"
            string_builder_temp += "    .packed-switch 0x0\n"
            string_builder_temp += "        :obf_pswitch_0\n"
            string_builder_temp += "    .end packed-switch\n"
            split_method_list.insert(-1, string_builder_temp) 

            final_obfuscated_method = split_method_list[:4]+ split_method_list[-2:]
        else:
            order_dict = {}
            for index, item in enumerate(order_list):
                order_dict[index] = item

            new_order_list = []

            for i in range(len(chunks_to_modify_list)):
                for k, v in order_dict.items():
                    if i == v:
                        new_order_list.append(chunks_to_modify_list[k])
                        break
            
            # Create default case 0, first chunk code of split code
            split_method_list[FIRST_CHUNK] = self.add_pswitch_const_goto(split_method_list[FIRST_CHUNK], 0, order_dict[0] + 1, locals_number)

            # Handle the rest of the switch cases
            for index, item in enumerate(new_order_list):
                for k, v in order_dict.items():
                    if v == index:
                        try:
                            next = order_dict[k+1] + 1
                            new_order_list[index] = self.add_pswitch_const_goto(item, index + 1, next, locals_number)
                        except KeyError as e:
                            new_order_list[index] = self.add_pswitch_const_goto(item, index + 1, -1, locals_number)
                        break
            # Create Switch table at the end
            string_builder_temp = "    :pswitch_obf\n"
            string_builder_temp += "    .packed-switch 0x0\n"
            for i in range(len(order_list) + 1):
                string_builder_temp += f"        :obf_pswitch_{i}\n"
            string_builder_temp += "    .end packed-switch\n"
            split_method_list.insert(-1, string_builder_temp) 
            final_obfuscated_method = split_method_list[:4] + new_order_list + split_method_list[-2:]

        
        return "\n".join(final_obfuscated_method)

    def obfuscate_smali_full(self):
        with open("obfused.smali", 'w') as f:
            f.write(self.get_imports() + "\n")

            for item in self.methods:
                f.write(self.method_obfuscator(item))

def main():
    o1 = ControlFlowObfuscation("MainActivity.smali")
    o1.obfuscate_smali_full()

if __name__ == "__main__":
    main()