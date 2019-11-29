import pkgutil
import re
from os import path
import shaonutil.file as f
import shaonutil.stats as i
import shaonutil
import shaonutil.file
import argparse


def get_all_submodules(packagename):
	package = __import__(packagename, fromlist="dummy")	
	prefix = package.__name__ + "."
	return [modname for importer, modname, ispackage in pkgutil.iter_modules(package.__path__, prefix)]


def import_all(packagename,log=False):
	for modname in get_all_submodules(packagename):
	    module = __import__(modname, fromlist="dummy")
	    if(log): print("Imported", module)


def get_file_description(i):
	i = __import__(i, fromlist="dummy")
	funcs = f.get_all_functions(i)
	func_doc_dic = {}

	for func in funcs:
		stri = 'i.'+func+'.__doc__'
		if eval(stri) != None:
			func_doc_dic[func] = eval(stri)

	func_string = ''
	for func in func_doc_dic:
		func_string += func + ' - ' + func_doc_dic[func] + '\n\n'

	return '### '+i.__doc__+'\n\n' + func_string

def main(filename,printl=False):
	func_string_final = ''
	for submod in get_all_submodules('shaonutil'):
		func_string_final += get_file_description(submod)

	start = '## Function Usages'
	end = 'Function Usages End'
	

	# read the contents of your README file
	this_directory = path.abspath(path.dirname(__file__))
	with open(path.join(this_directory, filename), encoding='utf-8') as file:
	    lines = file.readlines()

	count = 0
	startc = 0
	endc = 0
	for c in lines:
		if start in c:
			startc = count
		if end in c:
			endc = count
			break
		count+=1

	alllines = ''.join(lines)
	function_usage_string = lines[startc+1:endc]
	deductlines = ''.join(function_usage_string)

	final_string_to_save = alllines.replace(deductlines,func_string_final)

	if(printl):print(final_string_to_save)
	shaonutil.file.write_file(filename, final_string_to_save,mode="w")

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("--readme", help="../shaonutil/README.md",type=str)
	args = parser.parse_args()
	if args.readme:
		filename = args.readme
	else:
		filename = '../shaonutil/README.md'

	main(filename)