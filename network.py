from enum import Enum
from abc import ABC, abstractmethod, abstractproperty
import numpy as np


class Lattice(Enum):
    LINE = 0
    SQUARE = 1
    RECTANGLE = 2
    TRIANGLE = 3
    HEXAGON = 4


class Network(ABC):

    def __init__(self, pitch: float, center: list[float, float] = [0, 0], angle: float = 0) -> None:
        self.pattern: Lattice
        self.pitch: float = pitch
        self.number: int
        self.coords: np.array[float, float]
        self.center: list[float, float] = np.array(center)
        self.angle: float = angle

    def _compute(self) -> None:
        self._compute_coords()
        if self.angle:
            self._rotate()
        self._add_offset()

    @abstractmethod
    def _compute_coords(self) -> None:
        """To be defined in subclass"""
        pass

    def _rotate(self) -> None:
        x = self.coords[:,0] * np.cos(self.angle) - self.coords[:,1] * np.sin(self.angle)
        y = self.coords[:,0] * np.sin(self.angle) + self.coords[:,1] * np.cos(self.angle)
        self.coords[:,0] = x
        self.coords[:,1] = y

    def _add_offset(self) -> None:
        self.coords += np.array(self.center)


class LinearNetwork(Network):

    def __init__(self, number: int, pitch: float, center: list[float, float] = [0, 0], angle: float = 0) -> None:
        super().__init__(pitch, center, angle)
        self.pattern = Lattice.LINE
        self.number: int = number
        self._compute()

    def _compute_coords(self) -> None:
        expansion = (self.number - 1) * self.pitch
        coords = np.zeros(shape=(self.number, 2))
        coords[:,0] = np.linspace(start=-expansion/2, stop=expansion/2, num=self.number)
        coords[:,1] = np.zeros(shape=(self.number))
        self.coords = coords
        

class SquareNetwork(Network):

    def __init__(self, size: int, pitch: float, center: list[float, float] = [0, 0], angle: float = 0) -> None:
        super().__init__(pitch, center, angle)
        self.pattern = Lattice.SQUARE
        self.size: int = size
        self.number: int = np.power(self.size, 2)
        self._compute()

    def _compute_coords(self) -> None:
        expansion = (self.size - 1) * self.pitch
        coords_1D = np.linspace(start=-expansion/2, stop=expansion/2, num=self.size)
        coords = np.zeros(shape=(self.number, 2))

        for row in range(self.size):
            for col in range(self.size):
                idx = np.ravel_multi_index(multi_index=([row], [col]), dims=(self.size, self.size))
                coords[idx,:] = [coords_1D[row], coords_1D[col]]
        self.coords = coords    


class RectangleNetwork(Network):

    def __init__(self) -> None:
        super().__init__()
        self.pattern = Lattice.RECTANGLE


class TriangleNetwork(Network):

    def __init__(self) -> None:
        self.pattern = Lattice.TRIANGLE
        return NotImplementedError
    

class HexagonalNetwork(Network):

    def __init__(self) -> None:
        self.pattern = Lattice.HEXAGON
        super().__init__()


if __name__ == "__main__":
    t = LinearNetwork(number=3, pitch=1)
    print(t.coords)

    t = SquareNetwork(size=3, pitch=1)
    print(t.coords)