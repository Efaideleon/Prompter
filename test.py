import unittest
from prompter import Size, PrompterLayoutManager, LayoutElement, Position


class TestRowContent(LayoutElement):
    def __init__(self, size=None):
        super().__init__(size=size)


class TestPrompterLayout(unittest.TestCase):
    def setUp(self):
        self.dimensions = Size(height=100.0, width=20.0)
        content1 = TestRowContent(size=Size(1, 5.0))
        content2 = TestRowContent(size=Size(1, 3.0))
        content3 = TestRowContent(size=Size(1, 8.0))
        self.row_content = [content1, content2, content3]
        self.layout = PrompterLayoutManager(self.row_content, self.dimensions)

    def test_build_rows(self):
        self.assertEqual(1, len(self.layout.rows))  # Expect 1 row based on content

    def test_set_row_positions(self):
        self.assertEqual(self.layout.rows[0].position.y, 25.0)

    def test_update_rows_positions(self):
        expected_position = Position(0, 25.0, 0)

        self.assertAlmostEqual(self.layout.rows[0].position.x, expected_position.x, places=6)
        self.assertAlmostEqual(self.layout.rows[0].position.y, expected_position.y, places=6)
        self.assertAlmostEqual(self.layout.rows[0].position.z, expected_position.z, places=6)

    def test_align_content(self):
        # Expected positions after alignment
        expected_position1 = Position(-5.5, 25, 0)  # Centered based on total width
        expected_position2 = Position(-1.5, 25.0, 0.0)
        self.assertAlmostEqual(self.layout.rows[0].elements[0].position.x, expected_position1.x, places=6)
        self.assertAlmostEqual(self.layout.rows[0].elements[0].position.y, expected_position1.y, places=6)
        self.assertAlmostEqual(self.layout.rows[0].elements[0].position.z, expected_position1.z, places=6)

        self.assertAlmostEqual(self.layout.rows[0].elements[1].position.x, expected_position2.x, places=6)
        self.assertAlmostEqual(self.layout.rows[0].elements[1].position.y, expected_position2.y, places=6)
        self.assertAlmostEqual(self.layout.rows[0].elements[1].position.z, expected_position2.z, places=6)


# Run the tests
if __name__ == '__main__':
    unittest.main()
