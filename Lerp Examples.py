# First we need some way to visualise.
import tkinter as tk
from math import ceil, sin, cos, tan, log, pi
from random import randrange

# Thank you to wikipedia for all the maths behind the spiral functions and the linear interpolation.


class Main(tk.Tk):
	def __init__(self, width = 350, height = 350):
		super().__init__()
		self.width = width
		self.height = height

		self.geometry(f"{width}x{height}")
		self.title("Linear Interpolation And Some Equations")
		self.canvas = tk.Canvas(bg = "black")
		self.canvas.place(x = 0, y = 0, width = width, height = height)
		self.lerpEnabled = True
		# And that's how we'll be displaying our data.
		self.createArt(noLerp = self.lerpEnabled)
		
		self.lerpToggleButton = tk.Button(text = "ON", command = self.toggleLerp)
		self.lerpToggleButton.place(x = 965, y = self.height / 2 - 25, width = 30)

	def toggleLerp(self):
		self.lerpEnabled = not self.lerpEnabled
		self.canvas.delete('all')

		if not self.lerpEnabled:
			self.lerpToggleButton["text"] = "ON"
		else:
			self.lerpToggleButton["text"] = "OFF"
		self.lerpToggleButton.pack_forget()
		self.createArt(noLerp = not self.lerpEnabled)
		self.lerpToggleButton.place(x = 965, y = self.height / 2 - 25, width = 30)

	def distance(self, a, b):
		return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5


	def spiral(self, radialFunction = (lambda radius, angle: radius), radius = 1, size= 500):
		data = []
		for i in range(size):
			try:
				x = radialFunction(radius, i) * cos(i / 10)
				y = radialFunction(radius, i) * sin(i / 10)
			except ZeroDivisionError:
				#print("F")
				continue
			data.append((x, y))
		return data
	
	def circle(self, radius = 1, size = 500):
		return self.spiral(radius = radius, size = size)

	def archimedeanSpiral(self, radius = 1, size = 500):
		return self.spiral(radius = radius, size = size, radialFunction = lambda radius, angle: radius * angle)
	
	def hyperbolicSpiral(self, radius = 1, size = 500):
		return self.spiral(radius = radius, size = size, radialFunction = lambda radius, angle: radius / angle)
	
	def fermatSpiral(self, radius = 1, size = 500):
		return self.spiral(radius = radius, size = size, radialFunction = lambda radius, angle: radius * (angle ** 0.5))
	
	def lituus(self, radius = 1, size = 500):
		return self.spiral(radius = radius, size = size, radialFunction = lambda radius, angle: radius * (1 / (angle ** 0.5)))

	def interpolateTwoDimensionalData(self, data, dotHalfSize):
		newData = []
		#lerpedValues = []
		dotSize = dotHalfSize * 2
		for i in range(len(data) - 1):
			newData.append(data[i])
			# That is the number of the dots needed. So we'll divide 1 by it, to get the dot depth.
			try:
				accuracy = 1.0 / (self.distance(data[i], data[i + 1]) / dotSize)
			except ZeroDivisionError:
				accuracy = 1.0 / 2
			# We will take it multiplied by 100, and get the value by that.
			for j in range(0, 100, int(ceil(accuracy * 100))):
				x = self.lerp(data[i][0], data[i + 1][0], j/100)
				y = self.lerp(data[i][1], data[i + 1][1], j/100)
				#lerpedValues.append((x,y))
				newData.append((x,y))
			newData.append(data[i + 1])

		return newData

	def interpolateTwoDimensionalDataTemp(self, data, dotHalfSize):
		newData = []
		#lerpedValues = []
		dotSize = dotHalfSize * 2
		for i in range(len(data) - 1):
			newData.append(data[i])
			# That is the number of the dots needed. So we'll divide 1 by it, to get the dot depth.
			try:
				accuracy = 1.0 / (self.distance(data[i], data[i + 1]) / dotSize)
			except ZeroDivisionError:
				accuracy = 1.0 / 2
			# We will take it multiplied by 100, and get the value by that.
			for j in range(0, 100, int(ceil(accuracy * 100))):
				x = self.lerp(data[i][0], data[i + 1][0], j/100)
				y = self.lerp(data[i][1], data[i + 1][1], j/100)
				#lerpedValues.append((x,y))
				newData.append((x,y))
			newData.append(data[i + 1])

		return newData
	def heart(self, size = 300):
		data = []
		for x in range(-100, 100):
			t = x / 100
			x = sin(t) * cos(t) * (log(abs(t)) if t != 0 else 1)
			y = (abs(t) ** 0.5) * cos(t)

			data.append((x * size,-y * size))
		return data  

	def sineWave(self, start = [0, 0], end = [100, 0], amplitude = 10, frequency = 0.5, phase = 0, rotation = 0):
		data = []

		for x in range(start[0], end[0]):
			y = amplitude * sin(2*pi*frequency * x + phase)

			#Thanks to Aryabhata from maths.stackechange.com for the following rotation maths.
			rotatedX = x * cos(rotation) - y * sin(rotation)
			rotatedY = x * sin(rotation) + y * cos(rotation)

			data.append((rotatedX, rotatedY))
		return data

	def createArt(self, noLerp = False):
		offset = (self.width / 2, self.height / 2)
		dotHalfSize = 2.5

		if noLerp:
			self.interpolateTwoDimensionalData = lambda data, dotHalfSize: data
		else:
			self.interpolateTwoDimensionalData = self.interpolateTwoDimensionalDataTemp

		data = self.heart()
		newData = self.interpolateTwoDimensionalData(data, 1)
		self.generateLine(newData, dotHalfSize = 2, colour = "red", offset = (150, 230))
		self.canvas.create_text(150, 280, fill="White", font="sans 20 bold", text="Heart")

		data = self.circle(radius = 100)
		newData = self.interpolateTwoDimensionalData(data, dotHalfSize)
		self.generateLine(newData, dotHalfSize = dotHalfSize, colour = "green", offset = (400, 130))
		self.canvas.create_text(400, 280, fill="White", font="sans 20 bold", text="Circle")

		data = self.archimedeanSpiral(radius = 1, size = 125)
		newData = self.interpolateTwoDimensionalData(data, dotHalfSize * 0.5)
		self.generateLine(newData, dotHalfSize = dotHalfSize, colour = "#6666FF", offset = (650, 130))
		self.canvas.create_text(650, 280, fill="White", font="sans 20 bold", text="Archimedean Spiral")

		data = self.hyperbolicSpiral(radius = 3000, size = 500)
		newData = self.interpolateTwoDimensionalData(data, dotHalfSize * 0.2)
		self.generateLine(newData, dotHalfSize = dotHalfSize, colour = "#FFFF00", offset = (150, 400))
		self.canvas.create_text(150, 500, fill="White", font="sans 20 bold", text="Hyperbolic Spiral")

		data = self.fermatSpiral(radius = 5, size = 250)
		newData = self.interpolateTwoDimensionalData(data, dotHalfSize * 0.5)
		self.generateLine(newData, dotHalfSize = dotHalfSize, colour = "#800080", offset = (400, 400))
		self.canvas.create_text(400, 500, fill="White", font="sans 20 bold", text="Fermat Spiral")

		data = self.lituus(radius = 700, size = 500)
		newData = self.interpolateTwoDimensionalData(data, dotHalfSize * 0.2)
		self.generateLine(newData, dotHalfSize = dotHalfSize, colour = "#FFA500", offset = (650, 400))
		self.canvas.create_text(650, 500, fill="White", font="sans 20 bold", text="Lituus")
		
		data = self.sineWave(start = [0, 0], end = [700, 0], amplitude = 15, frequency = 0.03, phase = 0, rotation = 90 * pi / 180)
		newData = self.interpolateTwoDimensionalData(data, 2)
		self.generateLine(data, dotHalfSize = 2, colour = "lightgreen", offset = (925, 0))

		straightLine = lambda x, rotation: (x * cos(rotation), x*sin(rotation))
		#For straight Line
		data = [straightLine(x, 87 * pi / 180) for x in range(0, 1000, 200)]
		data = self.interpolateTwoDimensionalData(data, dotHalfSize = 0.1)
		self.generateLine(data, dotHalfSize = 2, colour = "lightblue", offset = (850, 0))

	def lerp(self, v0, v1, t):
		return (1 - t) * v0 + t* v1

	def generateLine(self, data, dotHalfSize = 1, offset = (0, 0), colour = "white"):
		for dot in data:
			self.canvas.create_oval(offset[0] - dotHalfSize + dot[0], 
									offset[1] - dotHalfSize + dot[1], 
									offset[0] + dotHalfSize + dot[0], 
									offset[1] + dotHalfSize + dot[1], 
									outline = colour, fill = colour)
main = Main(width = 1000, height = 600)
main.mainloop()







