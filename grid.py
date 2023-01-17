import numpy as np


class Grid_1D(object):
    default_size: int = 101
    default_expansion: tuple[float, float] = (-1.0, 1.0)

    def __init__(self,
        size: int = default_size,
        expansion: tuple[float, float] = default_expansion,
        ) -> None:

        self.dimension: int = 1
        self.points: int = size
        self.size: int = self.points
        self.expansion: tuple[float, float] = expansion
        self.coords: np.array = np.linspace(start=self.expansion[0], stop=self.expansion[1], num=self.size)

    @property
    def indexes(self) -> np.array:
        return np.arange(stop=self.points+1)

    @property
    def center(self) -> float:
        return np.mean(self.expansion)

    @property
    def span(self) -> float:
        return np.abs(self.expansion[1] - self.expansion[0])
    
    @property
    def step(self) -> float:
        return self.span / self.points
    
    @property
    def start(self) -> float:
        return self.expansion[0]
    
    @property
    def stop(self) -> float:
        return self.expansion[1]
    
    def __str__(self) -> str:
        return f"""
        {self.dimension}D Grid:
        - Points: {self.points}
        - Start, Stop: {self.start, self.stop}
        - Span, Step: {self.span, self.step}
        """



class Grid_ND(object):
    default_size: tuple[int, int] = 101
    default_expansion: tuple[float, float] = (-1.0, 1.0)

    def __init__(self,
        dimension: int = 2,
        sizes: list[int] = default_size,
        expansions: list[tuple[float, float]] = default_expansion,
        ) -> None:

        self.dimension: int = dimension
        self._check_inputs(sizes=sizes, expansions=expansions)
        self.points = np.prod(self.sizes)
        self._grid = [Grid_1D(size=self.sizes[i], expansion=self.expansions[i]) for i in range(self.dimension)]
        self._compute_coords()

    def _check_inputs(self, sizes: list[int], expansions: list[tuple[float, float]]):
        self._check_size(sizes=sizes)
        self._check_expansion(expansions=expansions)

    def _check_size(self, sizes: list[int]) -> None:
        self.sizes = self._check_input_dimensionality(input=sizes)

    def _check_input_dimensionality(self, input) -> list:
        try:
            dim = len(input)
        except TypeError:
            dim = []

        if dim:
            if len(input) >= self.dimension:
                output = [input[i] for i in range(0, self.dimension)]
            else:
                output = []
                for i in range(0, self.dimension):
                    if i in range(0, len(input)):
                        output.append(input[i])
                    else:
                        output.append(input[-1])
        else:
            output = [input for _ in range(0, self.dimension)]
        return output

    def _check_expansion(self, expansions: list[tuple[float, float]]) -> None:
        if isinstance(expansions, list):
            self.expansions = self._check_input_dimensionality(input=expansions)
        else:
            self.expansions = [expansions for _ in range(self.dimension)]

    def _compute_coords(self) -> None:
        grids_coords = tuple([self._grid[i].coords for i in range(self.dimension)])
        self.coords = np.meshgrid(*grids_coords)

    @property
    def indexes(self) -> np.array:
        return [self._grid[i].indexes for i in range(self.dimension)]

    @property
    def center(self) -> float:
        return [self._grid[i].center for i in range(self.dimension)]

    @property
    def span(self) -> float:
        return [self._grid[i].span for i in range(self.dimension)]
    
    @property
    def step(self) -> float:
        return [self._grid[i].step for i in range(self.dimension)]
    
    @property
    def start(self) -> float:
        return [self._grid[i].expansion[0] for i in range(self.dimension)]
    
    @property
    def stop(self) -> float:
        return [self._grid[i].expansion[1] for i in range(self.dimension)]
    
    def __str__(self) -> str:
        return f"""
        {self.dimension}D Grid:
        - Points: {self.points}
        - Sizes: {self.sizes}
        - Starts, Stops: {self.start, self.stop}
        - Spans, Steps: {self.span, self.step}
        """



if __name__ == "__main__":
    u = Grid_1D()
    print(u)

    v = Grid_ND(dimension=2, sizes=3)
    print(v)
    print(v._grid[0].coords)
    print(v.coords)
