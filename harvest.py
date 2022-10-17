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
        try:os.system(f"touch {self.function_file}")
        except:pass
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
                try:from pprint import pprint
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

    def collect(self, funct_dict:dict):
        """ append all functions from dictionary to file """

        f = open(self.function_file, 'a')
        for function in funct_dict.items():
            print(function)
            mylines = function['lines']

        f.close()

    def extract(self, filename):
        """ extract all the functions from a file and return it as a dictionary """
        if filename == None:
            return None
        else:
            fx = self.__findFunctions(filename)
            return fx

    def addFunction(self, function_name, function_file):
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
        
        myfunctions = {}
        
        pyfiles = self.allPythonFilepaths()
        f = open(self.function_file, 'a')

        for pyfile in pyfiles:
            funs = self.extract(pyfile)
            for k, v in funs.items():
                mylines = funs[k]["lines"]
                f = open(self.function_file, 'a')
                for line in mylines:
                    f.write(line)
                f.close()


        
        
    
    def allPythonFiles(self, verbose=True):
        """ get a list of all python files on your computer  """
        python_files = []
        filecount = 0
        pythonfile = {}
        for root, dirs, files in os.walk("/", topdown=False):
            for file in files:
                if file.endswith(".py"):
                    python_files.append(file)
                    filecount+=1
        newlist = []
        print(pythonfile)
        newfilecount = 0
        for x in python_files:
            if x == "__init__.py":
                pass 
            else:
                newlist.append(x)
                newfilecount+=1
        return newlist
    
    def showAlphabetical(self):
        files = self.allPythonFiles()
        xfiles = files
        mfiles = []
        for x in "abcdefghijklmnopqrstuvwxyz":
            for file in files:
                if file.startswith(x):
                    mfiles.append(file)
        for file in mfiles:
            print(file)

    def allPythonFilepaths(self):
        python_filepaths = []
        filecount = 0
        pythonfile = {}
        for root, dirs, files in os.walk("/", topdown=False):
            for file in files:
                if file.endswith(".py"):
                    filepath = root + "/" + file
                    print(filepath)
                    python_filepaths.append(filepath)
                    filecount+=1

        return python_filepaths
    

if __name__ == "__main__":
    harvest = FunctionHarvest()
    harvest.harvest()

