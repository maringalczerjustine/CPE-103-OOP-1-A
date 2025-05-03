class RegularPolygon:
      def __init__(self, side):
           self.side = side

class Square(RegularPolygon):
      def area(self):
           return self.side * self.side

class EquilateralTriangle(RegularPolygon):
      def area(self):
           return self.side * self.side * 0.4333

obj1 = Square(4)
obj2 = EquilateralTriangle(3)

print(obj1.area())
print(obj2.area())