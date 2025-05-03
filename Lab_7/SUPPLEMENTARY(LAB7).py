import math

class RegularPolygon:
      def __init__(self, side):
           self.side = side

class Square(RegularPolygon):
      def area(self):
           return self.side * self.side

class EquilateralTriangle(RegularPolygon):
      def area(self):
           return self.side * self.side * 0.4333

class Triangle(RegularPolygon):
      def area(self):
           return self.side * self.side * 0.5

class Pentagon(RegularPolygon):
      def area(self):
           return (1/4) * math.sqrt(5*(5 + 2 * math.sqrt(5))) * self.side * self.side

class Octagon(RegularPolygon):
      def area(self):
           return 2 * (1 + math.sqrt(2)) * self.side * self.side

obj1 = Square(4)
obj2 = EquilateralTriangle(3)
obj3 = Triangle(5)
obj4 = Pentagon(5)
obj5 = Octagon(8)

print("The area of Square is: ", obj1.area())
print("The areas of Equilateral Triangle is: ", obj2.area())
print("The area of Triangle is: ", obj3.area())
print("The area of Pentagon is: ", obj4.area())
print("The area of Octagon is: ", obj5.area())