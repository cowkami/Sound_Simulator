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
        shape: Tuple[Number, Number, Number] = (5, 4, 3),
        max_frequency: Number = 1.0e+3,
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
        shape: Tuple[Number, Number, Number], default (5, 4, 3)
            (x, y, z), lengths of the FDTD space.

        temperature: float, default 25.0
            temperature of the space.

        speed_sound: float or None, default 331.5 + 0.61 * temperature
            speed of sound traveling in the space.

        grid_spacing: float, default 0.01
            distance between the grid cells.
        
        time_step: float
            

        """
        self.Nx, self.Ny, self.Nz = shape
        self.T = temperature
        self.C = 331.5 + 0.61 * self.T if speed_sound is None else speed_sound
        self.dh = grid_spacing
        self.dt = time_step
        self.D = 

    def _handle_distance(self, distance: Number) -> int:
        """ transform a distance to an integer number of gridpoints """
        if not isinstance(distance, int):
            return int(float(distance) / self.grid_spacing + 0.5)
        return distance

    def _handle_time(self, time: Number) -> int:
            """ transform a time value to an integer number of timesteps """
            if not isinstance(time, int):
                return int(float(time) / self.time_step + 0.5)
            return time

    def _handle_tuple(
        self,
        shape: Tuple[Number, Number, Number]
    ) -> Tuple[int, int, int]:
        """ validate the grid shape and transform to a length-3 tuple of ints """
        x, y, z = shape
        x = self._handle_distance(x)
        y = self._handle_distance(y)
        z = self._handle_distance(z)
        return x, y, z

    def _handle_slice(self, s: slice) -> slice:
        """ validate the slice and transform possibly float values to ints """
        start = (
            s.start
            if not isinstance(s.start, float)
            else self._handle_distance(s.start))
        stop = (
            s.stop
            if not isinstance(s.stop, float) 
            else self._handle_distance(s.stop))
        step = (
            s.step
            if not isinstance(s.step, float)
            else self._handle_distance(s.step))
        return slice(start, stop, step)

    def _handle_single_key(self, key):
        """ transform a single index key to a slice or list """
        try:
            len(key)
            return [self._handle_distance(k) for k in key]
        except TypeError:
            if isinstance(key, slice):
                return self._handle_slice(key)
            else:
                return [self._handle_distance(key)]
        return key