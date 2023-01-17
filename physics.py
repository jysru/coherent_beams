import numpy as np

class Constants:
    c = 3e8


class Wavelength(object):
    default_wavelength = 980e-9

    def __init__(self, wavelength: float = default_wavelength) -> None:
        self.wavelength = wavelength
    
    @property
    def frequency(self) -> float:
        return Constants.c / self.wavelength
    
    @property
    def pulsation(self) -> float:
        return 2 * np.pi * self.frequency
    
    @property
    def period(self) -> float:
        return 1 / self.frequency
    
    @property
    def wavenumber(self) -> float:
        return 2 * np.pi / self.wavelength
    
    @property
    def spatial_frequency(self) -> float:
        return 1 / self.wavelength

    def __str__(self) -> str:
        return f"""
        Wavelength: {self.wavelength * 1e9 :.3f} [nm]
            - Wavenumber: {self.wavenumber / 1e2 :.3f} [rad/cm]
            - Spatial frequency: {self.spatial_frequency / 1e2 :.3f} [1/cm]
            - Frequency: {self.frequency * 1e-12 :.3f} [THz]
            - Pulsation: {self.pulsation / 1e15 :.3f} [rad/fs]
            - Period: {self.period * 1e15 :.3f} [fs]
        """


if __name__ == "__main__":
    print(Wavelength(wavelength=600e-9))
