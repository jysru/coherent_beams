from enum import Enum
import numpy as np

from physics import Wavelength


class BeamShape(Enum):
    TOP_HAT = 0
    GAUSSIAN = 1
    AIRY = 2
    LP = 3
    LG = 4



class Field(object):
    default_wavelength = 980e-9
    default_size = 100

    def __init__(self,
            size: tuple[int, int] = (default_size, default_size),
            wavelength: float = default_wavelength,
            ) -> None:
        self.size: tuple[int, int] = size
        self.field: np.array = np.zeros(shape=self.size)
        self.wavelength: Wavelength = Wavelength(wavelength=wavelength)

    @classmethod
    def intensity(self):
        return np.square(np.abs(self.field))
    
    @property
    def phase(self):
        return np.angle(self.field)
    
    def __str__(self) -> str:
        return f"""
        Field:
        - Wavelength: {self.wavelength.wavelength*1e9:.2f} [nm]
        - Size: {self.size[0]} x {self.size[1]} px
        """

    


class Beam(Field):
    default_min_range = 1e-4

    def __init__(self,
            type: BeamShape = BeamShape.GAUSSIAN,
            amplitude: float = 1,
            piston: float = 0,
            center: tuple[float, float] = 0,
            ) -> None:
        super(Field, self).__init__()
        self.type: BeamShape = type
        self.amplitude: float = amplitude
        self.center: tuple[float, float] = center
        self.piston: float = piston

    def _compute(self):
        return NotImplementedError
    
    def __str__(self) -> str:
        return super(Field, self).__str__()
    


if __name__ == "__main__":
    f = Field()
    print(f)

    b = Beam()
    print(b.size)


