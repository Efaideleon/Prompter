from abc import ABC, abstractmethod
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


class RowAligner(ABC):
    """Aligns elements in a row."""
    @abstractmethod
    def align_elements(self, row: 'Row'):
        """Align elements in a row."""
        pass


class AlignCenterRow(RowAligner):
    """Aligns Row elements to the center."""
    def align_elements(self, row: 'Row'):
        """Aligns all the elements in the row to the middle."""
        left = -(row.half_width())

        for element in row.elements:
            element.position.x = left + element.half_width()
            element.position.y = row.position.y
            left += element.size.width


class ElementLoadingError(Exception):
    pass


class ElementLoader(ABC):
    """Loads elements in a layout."""
    @abstractmethod
    def load_elements(self, layout: 'Layout', elements: List[LayoutElement]):
        """Loads elements into rows.

        Raises:
            ElementLoadingError: If an element is not added successfully into a Row.
        """
        pass


class LimitedRowWidthLoader(ElementLoader):
    """Loads elements into rows with a fixed maximum width."""
    def load_elements(self, layout: 'Layout', elements: List[LayoutElement]):
        """Loads elements into rows with a limited width."""
        for element in elements:
            if element.size.width > layout.size.width:
                raise ElementLoadingError(f"Element width: {element.size.width} exceeds max width: {layout.size.width}")

            if layout.rows[-1].size.width + element.size.width > layout.size.width:
                layout.rows.append(Row())

            layout.rows[-1].add_element(element)


class RowStacker(ABC):
    """Stack elements in a layout."""
    @abstractmethod
    def stack(self, layout: 'Layout', spacing_factor: float, start_factor: float):
        """Stacks rows in a layout."""
        pass


class VerticalRowStacker(RowStacker):
    def stack(self, layout: 'Layout', start_factor, spacing_factor):
        """Stacks the rows in the layout in a vertical order"""
        for i, row in enumerate(layout.rows):
            # Calculating the position using a linear rate y = mx + b
            row.position.y = -i * layout.size.height * spacing_factor + layout.size.height * start_factor


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

    def align_elements(self, aligner: RowAligner):
        """Aligns all the elements in the row to the middle."""
        aligner.align_elements(self)


class Layout:
    """Handles how the elements are loaded into the rows and their position."""
    def __init__(
            self,
            content: List[LayoutElement],
            size: Size,
            loader: ElementLoader,
            rows_stacker: RowStacker,
            row_aligner: RowAligner
    ):
        self.size = size
        self._content = content
        self.rows: List[Row] = [Row()]
        self._loader = loader
        self._rows_stacker = rows_stacker
        self._row_aligner = row_aligner

    def load_elements(self, elements: List[LayoutElement]):
        """Load elements into rows."""
        self._loader.load_elements(self, elements)

    def stack_rows(self, start_factor: float, spacing_factor: float):
        """Stacks rows based on a given RowStacker"""
        self._rows_stacker.stack(self, start_factor, spacing_factor)

    def align_rows_content(self):
        """Aligns the elements in a row based on a RowAligner"""
        for row in self.rows:
            row.align_elements(self._row_aligner)
