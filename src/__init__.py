import os ,subprocess
DEBUG = True
def main():
	if not DEBUG:
		subprocess.run(['cls'] , shell = True)
	try:
		import Path_GUI # main file 
	except:
		print(f'>>> -- Corrupt file --\n\n\r\
>>> Make sure Main.py is placed in ->{os.getcwd()}\\' ,end = '\n\n\r')

if __name__ == '__main__':
	main()