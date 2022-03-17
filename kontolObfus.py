import re

class ControlFlowObfuscation:
    def __init__(self, filename):
        self.filename = filename

        # Read Smali file
        with open(self.filename, "r") as f:
            self.content = f.read()
            

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

        # Split method into single lines and append them to a string but break with .line is found
        split_method_lines = method.splitlines()
        function_declaration = split_method_lines[0]
        end_method = split_method_lines[-1]

        for line in split_method_lines[1:-1]:
            if line.startswith('    .line'):
                split_method_list.append(temp_method_chunk_builder)
                temp_method_chunk_builder = ""

            temp_method_chunk_builder += line
        split_method_list.append(temp_method_chunk_builder)

        # Add back method declaration and end method
        split_method_list.insert(0, function_declaration)
        split_method_list.append(end_method)

        print(split_method_list)

        




def main():
    o1 = ControlFlowObfuscation("MainActivity.smali")
    o1.split_method_by_line("test")

if __name__ == "__main__":
    main()