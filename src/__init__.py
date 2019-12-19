import os ,subprocess
DEBUG = False

def print_Info():
	with open ('static/fancy.txt' ,'r') as dsgn:
		for line in dsgn :
			print('  '*4 ,end = '')
			print(line.strip())

def main():
	# initialization
	if not DEBUG:
		subprocess.run(['cls'] , shell = True)

	# logo onscr
	print_Info()
	
	try:# main
		import Path_GUI # main file 

	except ModuleNotFoundError as M:
		print(f'>>> -- Corrupt file --\n\n\r\
>>> Make sure Main.py is placed in ->{os.getcwd()}\\' ,end = '\n\n\r')
	finally:# not needed
		exit()

if __name__ == '__main__':
	main()