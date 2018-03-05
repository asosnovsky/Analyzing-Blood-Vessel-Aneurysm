# Methods - Calc
from numpy import ndarray
from numpy import pi, abs
from numpy import arccos, clip, dot
from numpy.linalg import norm

def unit_vector(vector: ndarray) -> ndarray:
    """ Returns the unit vector of the vector.  """
    return vector / norm(vector)

def angle_between(v1:ndarray, v2:ndarray) -> float:
    """ Returns the angle in radians between vectors 'v1' and 'v2'::
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return arccos(clip(dot(v1_u, v2_u), -1.0, 1.0))

def check_parallel(a:ndarray, b:ndarray, epsilon:float = EPSLION) -> (bool, float):
    """Determines if two lines are parallel, return bool, and angle
    """
    theta = angle_between(a,b)
    return (theta < epsilon) or (abs(theta - pi) < epsilon), theta
