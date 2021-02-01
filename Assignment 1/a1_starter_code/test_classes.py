import unittest


import a1


class TestA1Classes(unittest.TestCase):

    def test_rectangle(self):
        """Provided test for is_rectangle in starter code."""
        tri_1 = a1.Polygon(3, [3, 4, 5])
        self.assertEqual(tri_1.is_rectangle(), False)
        rect = a1.Polygon(4, angles=[90, 90, 90, 90])
        self.assertEqual(rect.is_rectangle(), True)
        diamond = a1.Polygon(4, [1, 1, 1, 1], [114, 66, 114, 66])
        self.assertEqual(diamond.is_rectangle(), False)

    def test_rhombus(self):
        """Provided test for is_rhombus in starter code."""
        diamond = a1.Polygon(4, [1, 1, 1, 1], [114, 66, 114, 66])
        self.assertEqual(diamond.is_rhombus(), True)
        rhomubs_1 = a1.Polygon(4, lengths=[1, 1, 1, 1], angles=None)
        self.assertEqual(rhomubs_1.is_rhombus(), True)

    def test_square(self):
        """Provided test for is_square in starter code."""
        rect = a1.Polygon(4, angles=[90, 90, 90, 90])
        self.assertEqual(rect.is_square(), None)
        diamond = a1.Polygon(4, [1, 1, 1, 1], [114, 66, 114, 66])
        self.assertEqual(diamond.is_square(), False)
        squre_1 = a1.Polygon(3, lengths=None, angles=None)
        self.assertEqual(squre_1.is_square(), False)
        squre_2 = a1.Polygon(4, lengths=None, angles=None)
        self.assertEqual(squre_2.is_square(), None)
        squre_3 = a1.Polygon(4, [1, 1, 1, 1])
        self.assertEqual(squre_3.is_square(), None)

    def test_regular_hexagon(self):
        """Provided test for is_regular_hexagon in starter code."""
        diamond = a1.Polygon(4, [1, 1, 1, 1], [114, 66, 114, 66])
        self.assertEqual(diamond.is_regular_hexagon(), False)
        hexagon_1 = a1.Polygon(6, [1] * 6)
        self.assertEqual(hexagon_1.is_regular_hexagon(), None)
        hexagon_2 = a1.Polygon(6, [1] * 6, [120] * 6)
        self.assertEqual(hexagon_2.is_regular_hexagon(), True)
        hexagon_3 = a1.Polygon(6, lengths=[5, 4, 4, 4, 4, 4], angles=None)
        self.assertEqual(hexagon_3.is_regular_hexagon(), False)
        hexagon_4 = a1.Polygon(6, lengths=None, angles=[119, 119, 119, 119, 119, 125])
        self.assertEqual(hexagon_4.is_regular_hexagon(), False)
        hexagon_4 = a1.Polygon(6, lengths=None, angles=[120, 120, 120, 120, 120, 120])
        self.assertEqual(hexagon_4.is_regular_hexagon(), None)

    def test_isosceles_triangle(self):
        """Provided test for is_isosceles_triangle in starter code."""
        tri_1 = a1.Polygon(3, [3, 4, 5])
        self.assertEqual(tri_1.is_isosceles_triangle(), False)
        tri_2 = a1.Polygon(3, angles=[60, 60, 60])
        self.assertEqual(tri_2.is_isosceles_triangle(), True)
        tri_3 = a1.Polygon(3, [4, 4, 5])
        self.assertEqual(tri_3.is_isosceles_triangle(), True)

    def test_equilateral_triangle(self):
        """Provided test for is_equilateral_triangle in starter code."""
        tri_2 = a1.Polygon(3, angles=[60, 60, 60])
        self.assertEqual(tri_2.is_equilateral_triangle(), True)
        tri_3 = a1.Polygon(3, lengths=None, angles=None)
        self.assertEqual(tri_3.is_equilateral_triangle(), None)
        tri_4 = a1.Polygon(3, lengths=[6, 6, 7], angles=None)
        self.assertEqual(tri_4.is_equilateral_triangle(), False)

    def test_scalene_triangle(self):
        """Provided test for is_scalene_triangle in starter code."""
        tri_1 = a1.Polygon(3, [3, 4, 5])
        self.assertEqual(tri_1.is_scalene_triangle(), True)
        tri_2 = a1.Polygon(3, angles=[60, 60, 60])
        self.assertEqual(tri_2.is_scalene_triangle(), False)
        tri_3 = a1.Polygon(3, lengths=None, angles=None)
        self.assertEqual(tri_3.is_scalene_triangle(), None)

if __name__ == '__main__':
    unittest.main()
