import numpy as np
import inspect
from playerlib.utils.utils import *

NaN = np.NAN

PROJECT_NAME = 'AlonPlayer'
BETA_VERSION = '0.0.1'
DEFAULT_VIDEO_FORMAT_LIST = ['.MP4', '.MKV', '.AVI', '.FLV', '.MOV', '.MPEG', '.3GP', '.WebM']
MULTITHREAD = get_max_threads() - 2


def check_constants():
    """
    功能：检查并输出constants
    参数：none
    返回值：print
    """
    frame = inspect.currentframe().f_back
    local_vars = frame.f_locals

    print("Constants:")
    for name, value in local_vars.items():
        if name.isupper() and not inspect.ismodule(value):
            print(f"{name}: {value}")


if __name__ == '__main__':
    check_constants()
