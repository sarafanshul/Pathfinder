try:
	from multiprocessing import Pool
	import pygame
	import sys
	import math
	from tkinter import *
	from tkinter import ttk
	from tkinter import messagebox
	import os
except:
	print('NOT ENOUGH RESOURCES ,\n Read requirements.txt')


# ----------__init__ MAIN ----------
width = 500
height = 500
cols = 50
grid = [0 for i in range(cols)]
row = 50
red = (234, 32, 39) # matt red
green = (237, 76, 103) # lamina's perimeter # using red
path_all = (5, 196, 107) # path (final) now green
grey = (1, 1, 1) # boundary MAIN's
boundary_sat = (25, 25, 25) # boundary shade
block_sat = 1 # block darkness
block_sat_2 = 1 # corner blocks 
mouse_line_col = (206, 214, 224) # line color of walls
starting_point_col = (255, 8, 127) # magenta
openSet = []
closedSet = []
w = width//row
h = height//cols
cameFrom = []
multi_process_pool = Pool() #implementation/Runtime Errors Occurring

# initialize 
screen = pygame.display.set_mode((width, height)) # 600 ,600

class spot:
	def __init__(self, x, y):
		self.i = x
		self.j = y
		self.f = 0
		self.g = 0
		self.h = 0
		self.neighbors = []
		self.previous = None
		self.obs = False
		self.closed = False
		self.value = 1

	def show(self, color, st):
		if self.closed == False :
			pygame.draw.rect(screen, color, (self.i * w, self.j * h, w, h), st)
			pygame.display.update()

	def path(self, color, st):
		pygame.draw.rect(screen, color, (self.i * w, self.j * h, w, h), st)
		pygame.display.update()

	def addNeighbors(self, grid):
		i = self.i
		j = self.j
		if i < cols-1 and grid[self.i + 1][j].obs == False:
			self.neighbors.append(grid[self.i + 1][j])
		if i > 0 and grid[self.i - 1][j].obs == False:
			self.neighbors.append(grid[self.i - 1][j])
		if j < row-1 and grid[self.i][j + 1].obs == False:
			self.neighbors.append(grid[self.i][j + 1])
		if j > 0 and grid[self.i][j - 1].obs == False:
			self.neighbors.append(grid[self.i][j - 1])


# create 2d array
for i in range(cols):
	grid[i] = [0 for i in range(row)]

# Create Spots
for i in range(cols):
	for j in range(row):
		grid[i][j] = spot(i, j)


# Set start and end node
start = grid[12][5]
end = grid[3][6]

# SHOW RECTANGLES
for i in range(cols):
	for j in range(row):
		grid[i][j].show(boundary_sat, block_sat) # grid boundaries

for i in range(0,row):
	grid[0][i].show(grey, 1)
	grid[0][i].obs = True
	grid[cols-1][i].obs = True
	grid[cols-1][i].show(grey,1)
	grid[i][row-1].show(grey, 1)
	grid[i][0].show(grey, 1)
	grid[i][0].obs = True
	grid[i][row-1].obs = True

def onsubmit():
	global start
	global end
	st = startBox.get().split(',')
	ed = endBox.get().split(',')

	start = grid[int(st[0])%cols][int(st[1])%row] # % for inlength data intake
	end = grid[int(ed[0])%cols][int(ed[1])%row]
	
	window.quit()
	window.destroy()

window = Tk()
label = Label(window, text='Start(x,y): ')
startBox = Entry(window)
label1 = Label(window, text='End(x,y): ')
endBox = Entry(window)
var = IntVar()
showPath = ttk.Checkbutton(window, text='Show Steps :', onvalue=1, offvalue=0, variable=var)

submit = Button(window, text='Submit', command=onsubmit)

showPath.grid(columnspan=2, row=2)
submit.grid(columnspan=2, row=3)
label1.grid(row=1, pady=3)
endBox.grid(row=1, column=1, pady=3)
startBox.grid(row=0, column=1, pady=3)
label.grid(row=0, pady=3)

window.update()
mainloop()

pygame.init()
openSet.append(start)

def mousePress(x):
	t = x[0]
	w = x[1]
	g1 = t // (width // cols)
	g2 = w // (height // row)
	acess = grid[g1][g2]
	if acess != start and acess != end:
		if acess.obs == False:
			acess.obs = True
			acess.show(mouse_line_col, 0)#

end.show(starting_point_col, 0)
start.show(starting_point_col, 0)

loop = True
while loop:
	ev = pygame.event.get()

	for event in ev:
		if event.type == pygame.QUIT:
			pygame.quit()
		if pygame.mouse.get_pressed()[0]:
			try:
				pos = pygame.mouse.get_pos()
				mousePress(pos)
			except AttributeError:
				pass
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				loop = False
				break

for i in range(cols):
	for j in range(row):
		grid[i][j].addNeighbors(grid)

def heurisitic(n, e):
	d = math.sqrt((n.i - e.i)**2 + (n.j - e.j)**2)
	#d = abs(n.i - e.i) + abs(n.j - e.j)
	return d


def main():
	end.show(starting_point_col, 0)
	start.show(starting_point_col, 0)
	if len(openSet) > 0:
		lowestIndex = 0
		for i in range(len(openSet)):
			if openSet[i].f < openSet[lowestIndex].f:
				lowestIndex = i

		current = openSet[lowestIndex]
		if current == end:
			print('done', current.f)
			start.show(starting_point_col,0)
			temp = current.f
			for i in range(round(current.f)):
				current.closed = False
				current.show(path_all, 0)
				current = current.previous
			end.show(starting_point_col, 0)

			Tk().wm_withdraw()
			result = messagebox.askokcancel('Program Finished', \
(f'The program finished, the shortest distance \n\
to the path is {int(temp)} blocks away, \
\n Would you like to re run the program?')
				)
			if result == True: # restart the program using exce function
				# The exec functions of Unix-like operating 
				# 	systems are a collection of functions that
				# 	causes the running process to be completely 
				# 	replaced by the program passed as an argument to the function
				os.execl(sys.executable,sys.executable, *sys.argv)
			else:
				pygame.quit()
				exit()
			pygame.quit()

		openSet.pop(lowestIndex)
		closedSet.append(current)

		neighbors = current.neighbors
		for i in range(len(neighbors)):
			neighbor = neighbors[i]
			if neighbor not in closedSet:
				tempG = current.g + current.value
				if neighbor in openSet:
					if neighbor.g > tempG:
						neighbor.g = tempG
				else:
					neighbor.g = tempG
					openSet.append(neighbor)

			neighbor.h = heurisitic(neighbor, end)
			neighbor.f = neighbor.g + neighbor.h

			if neighbor.previous == None:
				neighbor.previous = current
	if var.get():
		for i in range(len(openSet)):
			openSet[i].show(green, 0)

		for i in range(len(closedSet)):
			if closedSet[i] != start:
				closedSet[i].show(red, 0)
	current.closed = True


while True:
	ev = pygame.event.poll()
	if ev.type == pygame.QUIT:
		pygame.quit()
	pygame.display.update()
	try: 
		main()
	except: 
		print('Computational Error Occured') 

exit()
