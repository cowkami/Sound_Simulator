from typing import Tuple


## Constants
TEMPERATURE: float = 25.0  # celcius degree
SPEED_SOUND: float = 331.5 + 0.61 * TEMPERATURE  # [m/s] speed of sound



class Grid(object):
    """
    The FDTD Grid
    """
    def __init__(
        self,
        shape: Tuple[int, int, int] = (500, 300, 100),
        temperature: float = 25.0,
        speed_sound: float = None,
        grid_spacing: float = 0.01,
        time_step: float = 20.0e-6,
        space_density: float = 1.2
    ):
        """
        initialize Grid class
        
        Parameters
        ----------
        shape: Tuple[int, int, int], default (500, 300, 100)
            (x, y, z), lengths of the FDTD space.

        temperature: float, default 25.0
            temperature of the space.

        speed_sound: float or None, default 331.5 + 0.61 * temperature
            speed of sound traveling in the space.

        grid_spacing: float, default 0.01
            distance between the grid cells.
        
        time_step:
            

        """
        self.T = temperature
        self.C = 331.5 + 0.61 * self.T if speed_sound is None else speed_sound
        self.dx = grid_spacing
        self.dt = time_step

