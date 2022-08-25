import math

class CPoint(object):
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return "[x:{0},y:{1},z:{2}]".format(self.x,self.y,self.z)

    def __add__(self,other):
        x = self.x + other.x
        y = self.y + other.y
        z = self.z + other.z
        return CPoint(x,y,z)

    def __sub__(self,other):
        x = self.x - other.x
        y = self.y - other.y
        z = self.z - other.z
        return CPoint(x,y,z)

    def distance(self,other):
        dist = self-other
        squaredsum = dist.x*dist.x + dist.y*dist.y + dist.z*dist.z
        actualdist = math.sqrt(squaredsum)
        return actualdist


LOCATIONS = {'door':CPoint(-8.18,-3.16,0.0), 'bigtankfront': CPoint(-4.07,-7.24,0.0),
             'bigtankside':CPoint(-7.25,-5.26,0.0), 'tank1top': CPoint(-0.49,-3.51,0.0),
             'tank1right': CPoint(2.30,-1.93,0.0), 'tank1bottom': CPoint(5.48,-3.48,0.0),
             'tank2top': CPoint(-0.47,-6.52,0.0), 'tank2left': CPoint(1.98,-7.88,0.0),
             'tank2bottom': CPoint(5.36,-6.31,0.0), 'tankset': CPoint(6.80,-5.69,0.0),
             'pipes': CPoint(7.79,-2.67,0.0), 'dangerroom': CPoint(1.30,2.20,0.0),
             'stairs': CPoint(2.94,8.56,0.0),
             'entrance':CPoint(-7.825369834899902, -0.5725803375244141, 0.02588939666748047),
             'dangerroomside':CPoint(-0.5568475723266602, 0.515995979309082, 0.00116729736328125),
             'dangerroomsideend':CPoint(4.197497367858887, 0.3372831344604492, 0.004076957702636719)
             }


