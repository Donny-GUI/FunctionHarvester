import os
import json


class Function:
    def __init__(self, name=None, args=None, flines=None):
        self.name = name
        self.flines = flines
        self.args = args

class Argument:
    def __init__(self, name=None, hint=None, default_value=None):
        self.name = name
        self.hint = hint
        self.default_value = default_value

class FunctionHarvest:
    def __init__(self):
        self.function_file = "xx.py"
        self.collected_functions = self.__findFunctions(self.function_file)

    
    def __parseFunctions(self, filename,slices):
        f = open(filename, 'r'); lines = f.readlines();funct = {}
        for x in slices:
            function = Function();start_line = int(x[0])
            start_flines = int(start_line); end_flines = int(int(x[1]) - 1)
            flines = lines[int(start_flines):int(end_flines)]
            name = lines[int(start_line)]
            xname = str(name)
            yname = xname[4:]
            zname = yname.split("(")
            args = zname[1]
            yargs = args.split('):')
            oargs = yargs[0]
            try:
                fargs = yargs[1].split("):")[0]
                zargs = yargs[0]
                targs = zargs.split("):")
                wargs = targs[0]
                try:
                    vargs = wargs.split(", ")
                    function.args = vargs
                except:function.args = wargs
            except:function.args = oargs
            wname = zname[0]
            function.name = wname
            function.flines = flines
            func = {}
            func['name'] = function.name
            func['lines'] = function.flines
            func['args'] = function.args
            func['file'] = filename
            funct[f'{function.name}'] = func
        return funct

    def __findFunctions(self, filename):
        imports =[]; function_slices = []; f = open(filename, 'r')
        lines = f.readlines(); current_function = []
        for index, line in enumerate(lines):
            if line.startswith("import "):
                imports.append(index)
            if line.startswith("def "):
                current_function.append(index)
                length_current_function = len(current_function)
                if length_current_function == 2:
                    function_slices.append(current_function)
                    current_function = [current_function[1]]
        f.close()
        fx = self.__parseFunctions(filename, function_slices)
        return fx

    def extract(self, filename):
        """ extract all the functions from a file and return it as a dictionary """
        if filename == None:
            return None
        else:
            fx = self.__findFunctions(filename)
            return fx

    def collect(self, function_name, function_file):
        """ Provide the function name and filename and it will add it to your list of functions """

        self.new_function = {}
        fx = self.extract(function_file)
        try:
            self.new_function = fx[f'{function_name}']
        except:
            print("bad function name")
            raise Exception("Function name not in extracted list of functions")
        f = open(self.function_file, 'a')
        f.write(self.new_function)
        f.write("\n")
        f.close()
        print(f"function: {function_name} added to your functions")

    def harvest(self, root="/"):
        """ scan the entire filesystem for python files, extract the functions from all files """
        python_files = []
        for root, dirs, files in os.walk(root, topdown=False):
            for file in files:
                if file.endswith(".py"):
                    python_files.append(file)
        newlist = []
        for x in python_files:
            if x not in newlist:
                newlist.append(x)
        print(newlist)
        


if __name__ == "__main__":
    harvest = FunctionHarvest()
    harvest.harvest()

