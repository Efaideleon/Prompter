from typing import List
from dataclasses import dataclass


@dataclass
class Size:
    """Represents the size of an element using height and width."""
    height: float
    width: float


@dataclass
class Position:
    """Represents the position of an element in 3D space."""
    x: float
    y: float
    z: float


class LayoutElement:
    """Base class of a layout element."""
    def __init__(self, size: Size):
        self.size = size
        self.position: Position = Position(0, 0, 0)

    def half_width(self) -> float:
        """Returns half the width of a layout element."""
        return self.size.width / 2


class Row(LayoutElement):
    """Represents a row element that contains layout elements."""
    def __init__(self):
        super().__init__(Size(0, 0))
        self.elements: List[LayoutElement] = []

    def add_element(self, element: LayoutElement):
        """Adds a layout elements to the row and updates the width."""
        self.elements.append(element)
        self._update_size()

    def _update_size(self):
        """Updates the current width taken by all the elements."""
        self.size.width = sum(element.size.width for element in self.elements)

    def align_elements_center(self):
        """Aligns all the elements in the row to the middle."""
        left = -(self.half_width())

        for element in self.elements:
            element.position.x = left + element.half_width()
            element.position.y = self.position.y
            left += element.size.width


class PrompterLayoutManager:
    """Handles how the elements are loaded into the rows and their position."""
    def __init__(
            self,
            content: List[LayoutElement],
            size: Size,
    ):
        self.size = size
        self._content = content
        self.rows: List[Row] = [Row()]
        self.load_elements(self._content)
        self.stack_rows_vertically(start_factor=0.25, spacing_factor=0.5)

    def load_elements(self, elements: List[LayoutElement]):
        """Loads elements into rows with a limited width"""
        for element in elements:
            if element.size.width > self.size.width:
                raise ValueError(f"Element width: {element.size.width} exceeds max width: {self.size.width}")

            if self.rows[-1].size.width + element.size.width > self.size.width:
                self.rows.append(Row())

            self.rows[-1].add_element(element)

    def stack_rows_vertically(self, start_factor: float, spacing_factor: float):
        """Stacks the rows in the layout in a vertical order"""
        for i, row in enumerate(self.rows):
            # Calculating the position using a linear rate y = mx + b
            row.position.y = -i * self.size.height * spacing_factor + self.size.height * start_factor
            row.align_elements_center()
