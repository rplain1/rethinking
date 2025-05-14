from rpy2.robjects.packages import importr
from rpy2.robjects import r
import rpy2_arrow.pyarrow_rarrow as pyra

import polars as pl

rethnking = importr("rethinking")
r_arrow = importr("arrow")


def r_to_py(str):
    r(str)
    r_obj = r["d"]
    _df = pyra.rarrow_to_py_table(r_arrow.as_arrow_table(r_obj))
    return pl.from_arrow(_df)
