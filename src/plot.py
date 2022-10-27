import logging
import numpy as np

class Plot:
    """
        ##  This 
        -   Parameters
    """
    def __init__(self) -> None:
        """
            Instance of Plot
            -   Paremeters
            -   History
        """
        ## Create a Plot instance
        self._center = None
        self._scale = None
        self._data = None


    def center(filename: str) -> tuple:
        """
            Calculates the center
            -   Parameters
            -   
        """
        try:
            ## TODO: Figure out how to calculate center from filename
            return (25, 25)

        except Exception as e:
            logging.error(e)

    def profile(data: np.ndarray, center: list, scale: int) -> None:
        """
            This method calculates the radial profile
            -   Parameters
            -   
        """
        try:
            return None
        except Exception as e:
            logging.error(e)