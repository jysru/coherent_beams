from enum import Enum
from abc import ABC, abstractmethod, abstractproperty
import numpy as np
import matplotlib.pyplot as plt


def rotate_coords(x: list, y: list, angle: float) -> tuple[list, list]:
    if not isinstance(x, np.ndarray):
        x = np.array(x)
    if not isinstance(y, np.ndarray):
        y = np.array(y)
    xp = x*np.cos(angle) - y*np.sin(angle)
    yp = x*np.sin(angle) + y*np.cos(angle)
    return xp, yp
        

class Lattice(Enum):
    LINE = 0
    SQUARE = 1
    RECTANGLE = 2
    TRIANGLE = 3
    HEXAGON = 4


class Network(ABC):

    def __init__(self, pitch: float, center: list[float, float] = [0, 0], angle: float = 0) -> None:
        self.lattice: Lattice
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
        x, y = rotate_coords(self.coords[:,0], self.coords[:,1], angle=self.angle)
        self.coords[:,0] = x
        self.coords[:,1] = y

    def _add_offset(self) -> None:
        self.coords += np.array(self.center)

    def show(self) -> None:
        plt.figure()
        plt.axis("equal")
        plt.scatter(x=self.coords[:,0], y=self.coords[:,1])
        plt.title(f"{self.lattice.name} lattice")
        plt.show()


class LinearNetwork(Network):

    def __init__(self, number: int, pitch: float, center: list[float, float] = [0, 0], angle: float = 0) -> None:
        super().__init__(pitch, center, angle)
        self.lattice = Lattice.LINE
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
        self.lattice = Lattice.SQUARE
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

    def __init__(self, sizes: tuple[int, int], pitch: tuple[float, float], center: list[float, float] = [0, 0], angle: float = 0) -> None:
        super().__init__(pitch, center, angle)
        self.lattice = Lattice.RECTANGLE
        self.size: tuple[int, int] = sizes
        self.number: int = np.prod(self.size)
        self._compute()

    def _compute_coords(self) -> None:
        expansion_x = (self.size[0] - 1) * self.pitch
        expansion_y = (self.size[1] - 1) * self.pitch
        coords_x = np.linspace(start=-expansion_x/2, stop=expansion_x/2, num=self.size[0])
        coords_y = np.linspace(start=-expansion_y/2, stop=expansion_y/2, num=self.size[1])
        coords = np.zeros(shape=(self.number, 2))

        for row in range(self.size[0]):
            for col in range(self.size[1]):
                idx = np.ravel_multi_index(multi_index=([row], [col]), dims=(self.size[0], self.size[1]))
                coords[idx,:] = [coords_x[row], coords_y[col]]
        self.coords = coords


class TriangleNetwork(Network):
    
    def __init__(self, size: int, pitch: tuple[float, float], center: list[float, float] = [0, 0], angle: float = 0) -> None:
        super().__init__(pitch, center, angle)
        self.lattice = Lattice.TRIANGLE
        self.size: int = size
        self.number: int = int(0.5 * self.size * (self.size + 1))
        self._compute()

    def _compute_coords(self) -> None:
        coords = np.zeros(shape=(self.number, 2))
        x, y = [], []
        height = np.sqrt(3)/2 * self.pitch * (self.size - 1)

        for line in range(0, self.size):
            y_line = np.sqrt(3)/2*self.pitch*line - height/2
            n_on_line = self.size - line
            for col in range(0, n_on_line):
                x_col = -(n_on_line - 1)*self.pitch/2 + col * self.pitch
                x.append(x_col)
                y.append(y_line)

        coords[:,0] = np.array(x)
        coords[:,1] = np.array(y)

        self.coords = coords
    

class HexagonalNetwork(Network):

    def __init__(self, rings: int, pitch: tuple[float, float], center: list[float, float] = [0, 0], angle: float = 0) -> None:
        super().__init__(pitch, center, angle)
        self.lattice = Lattice.HEXAGON
        self.rings: int = rings
        self.diagonal: int = 1 + 2*self.rings
        self.number: int = int((np.power((6*self.rings + 3)/np.sqrt(3), 2)+1)/4)
        self._compute()

    def _compute_coords(self) -> None:
        coords = np.zeros(shape=(self.number, 2))
        x = []
        y = []

        k = 0
        for i in range(self.rings, -1, -1):
            ylin = np.sqrt(3)*i*self.pitch/2
            for j in range(1, (2*self.rings+2-i)):
                k += 1
                x.append( (-(2*self.rings-i+2)*self.pitch)/2 + j*self.pitch )
                y.append( ylin )
        
        x_tmp = np.array( x[0 : int((self.number-1)/2 - self.rings)] )
        y_tmp = np.array( y[0 : int((self.number-1)/2 - self.rings)] )

        x_tmp, y_tmp = rotate_coords(x_tmp, y_tmp, angle=np.pi)

        xx = np.concatenate((np.array(x), np.flip(x_tmp)))
        yy = np.concatenate((np.array(y), np.flip(y_tmp)))
        
        coords[:, 0] = xx
        coords[:, 1] = yy

        self.coords = coords


if __name__ == "__main__":
    # t = LinearNetwork(number=3, pitch=1)
    # t = SquareNetwork(size=3, pitch=1)
    # t = RectangleNetwork(sizes=(2,3), pitch=1)
    # t = HexagonalNetwork(rings=3, pitch=1)
    # t.show()

    t = TriangleNetwork(size=3, pitch=1)
    t.show()