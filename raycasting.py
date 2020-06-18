from tkinter import *
import random
import math
"""
Took me way to long to make. Still an disgusting mess. Definitely needs a revisit/total remake.
"""
root = Tk()
root.title("Rays")
root.geometry("1920x1010")

width, height = 1910, 1000
c = Canvas(root, width=width, height=height, bg="#000000")

#returns point of intersection between 2 lines. line = ((x,y)(x2,y2))
def line_intersection(line1, line2):
    x1 = line1[0][0]
    y1 = line1[0][1]
    x2 = line1[1][0]
    y2 = line1[1][1]

    x3 = line2[0][0]
    y3 = line2[0][1]
    x4 = line2[1][0]
    y4 = line2[1][1]

    denom = int((x1-x2)*(y3-y4)-(y1-y2)*(x3-x4))

    if denom == 0:
        return None
    else:
        t = ((x1-x3)*(y3-y4)-(y1-y3)*(x3-x4))/denom
        u = -((x1-x2)*(y1-y3)-(y1-y2)*(x1-x3))/denom

        if t > 0 and t < 1 and u > 0:

            x = x1+t*(x2-x1)
            y = y1+t*(y2-y1)

            if y > y4:
              return None 

            return [x,y]

#draws an oval at the given position
def oval(x,y,leng=5):
    oval = [((x-leng,y-leng),(x+leng,y+leng))] 

    x1 = oval[0][0][0]
    y1 = oval[0][0][1]
    x2 = oval[0][1][0]
    y2 = oval[0][1][1]
    o = c.create_oval(x1,y1,x2,y2, width=0, fill="white")
    c.pack()

#updates the rays 
def rays(x1,y1,lines1):
    lines = []
    intersectionslines = []
    newlist = []
    templist = []
    rays = []
    hyp = 2000 
    deg = 360/360
    for i in range(round(360/deg)):
        sin = math.sin(math.radians(i*deg-90))
        cath = hyp*sin
        aath = math.sqrt(hyp**2-cath**2)

        if i < round(360/deg/2)+1:
            x2,y2 = x1+aath,y1+cath
            lines.append(((x1,y1),(x2,y2)))
        else:
            x2,y2 = x1-aath,y1+cath
            lines.append(((x1,y1),(x2,y2)))
    counter = 0
    for line in lines:
        for linel in lines1:
            coords = line_intersection(line,sortline(linel))
            if coords == None:
                pass
            else:
                templist.append((coords[0],coords[1]))
        while len(templist) > 1:
            if shorterpoint(line[0],templist[0],templist[1]) is True:
                templist.pop(1)
            else:
                templist.pop(0)
        rays.append(templist)
        if len(templist) != 0:
            l = c.create_line(line[0][0], line[0][1], templist[0][0], templist[0][1], width=1, fill="#FFFFFF")
            templist = []
            rays = []
        else:
            templist = []
            rays = []

#im not sure if i even needed this, it sorts the points in a line by size (swaps them if necessary)
def sortline(line):
    x1 = line[0][0]
    y1 = line[0][1]
    x2 = line[1][0]
    y2 = line[1][1]

    if y1 < y2:
        return line
    elif y1 > y2:
        return ((x2,y2),(x1,y1))
    elif y1 == y2:
        if x1 < x2:
            return line
        else:
            #there was a bug with rays not being displayed/casted properly if they hit a horizontal line below their origin
            return ((x2+1,y2+1),(x1-1,y1-1))


#looks what point is closer to point1 and returns True or False
def shorterpoint(point1,point2,point3):
    x1 = point1[0]
    y1 = point1[1]

    x2 = point2[0]
    y2 = point2[1]

    x3 = point3[0]
    y3 = point3[1]
    leng1 = math.sqrt((x2-x1)**2+(y2-y1)**2)
    leng2 = math.sqrt((x3-x1)**2+(y3-y1)**2)

    if leng1 >= leng2:
        return False
    else:
        return True

#draws the INTERSECTION lines, lines our rays can intersect with
def drawintlines(lines):
    for line in lines:
        l = c.create_line(line[0][0],line[0][1],line[1][0],line[1][1],width=1,fill="#efefef")

#boundaries etc
walls = [((0,-5),(1,height+6)),((-5,-1),(width+6,0)),((width+1,-5),(width,height+6)),((-5,height+1),(width+6,height))]
global intersectlines
intersectlines = []
for n in range(5):
    intersectlines.append(((random.randint(40,width-40),random.randint(40,height-40)),(random.randint(40,width-40),random.randint(40,height-40))))
intersectlines += walls

#moves the origin of the raycaster in an oval orbit around the center
def movecircle(x1,y1,degr):
    hyp = 500 
    deg = 360/360
    sin = math.sin(math.radians(degr*deg-90))
    cath = hyp*sin
    aath = math.sqrt(hyp**2-cath**2)
    if degr < round(360/deg/2)+1:
        x2,y2 = x1+aath,y1+cath
    else:
        x2,y2 = x1-aath,y1+cath
    return x2*1.2,y2,degr+1

#COMMENT THIS OUT AND ENABLE THE CODE BELOW TO CHANGE INTO MOUSE MOVEMENT INSTEAD OF AN ORBITAL MOVEMENT
degr = 0
x = round(width/2)
y = round(height/2)
while True:
    if degr > 360:
        degr = 0
    c.delete("all")
    drawintlines(intersectlines)
    x1,y1,degr = movecircle(x,y,degr)[0],movecircle(x,y,degr)[1],movecircle(x,y,degr)[2] 
    print(f"x={x},y={y}")
    rays(x1,y1,intersectlines)

    c.pack()
    root.update()

"""
def motion(event):
    x, y = event.x, event.y
    c.delete("all")
    rays(x,y,lines1=intersectlines)
    drawintlines(intersectlines)
    c.pack()

root.bind('<Motion>', motion)
c.pack()
root.mainloop()
"""



"""
                                                        created by jax0033@protonmail.com
"""
