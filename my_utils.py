from rpy2.robjects.packages import importr
from rpy2.robjects import r
import rpy2_arrow.pyarrow_rarrow as pyra

import polars as pl

rethnking = importr("rethinking")
r_arrow = importr("arrow")

RED = "#E37"
BLUE = "C0"


def r_to_py(str, env_var="d"):
    r(str)
    r_obj = r[env_var]
    _df = pyra.rarrow_to_py_table(r_arrow.as_arrow_table(r_obj))
    return pl.from_arrow(_df)
