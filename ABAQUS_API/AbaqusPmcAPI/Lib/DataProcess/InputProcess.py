import numpy as np
import pandas as pd
from scipy import interpolate
from Lib.Common.basicFunction import *


def countList(lst1, lst2):
    return [sub[item] for item in range(len(lst2)) for sub in [lst1, lst2]]


def convert_csv_dataframe(filepath, col):
    with open(filepath, "r+") as file:
        lines = file.readlines()
        data = []
        for i, line in enumerate(lines):
            if i > 4:
                nums = [i for i in line.strip().split(' ') if i != '' and i != 'X']
                if len(nums) <= 2:
                    data.append(nums)
        df = pd.DataFrame(data, columns=col)
        df.dropna(inplace=True)
        df = df.astype('float')
    return df

def modify_macros_py_code(file_path, input_file):
    prefix = ['_loading_pt', '_pt1', '_K']
    with open('./Lib/AbaqusPy/abaqusMacros.py', "r+") as file:
        prefix_idx = 0
        lines = file.readlines()
        new_lines = []
        for line in lines:
            if ".odb" in line:
                idx = [i for i, c in enumerate(line) if c == "'"]
                line = line[:idx[0]] + "'" + file_path + "\\" + input_file + ".odb'" + line[idx[-1] + 1:]
            if ".csv" in line:
                idx = [i for i, c in enumerate(line) if c == "'"]
                line = line[:idx[0]] + "'" + file_path + "\\" + "Result" + "\\" + input_file + prefix[prefix_idx] + ".csv'" + line[idx[-1] + 1:]
                prefix_idx += 1
            new_lines.append(line)
        new_line = ''.join(new_lines)
        file.seek(0)
        file.truncate()
        file.write(new_line)
        file.close()


def find_start_end_time(data_lines):
    data_lines = ''.join(data_lines)
    data_temp = data_lines.replace('\n', ',')
    data = data_temp.split(',')
    start = float(data[0])
    end = float(data[-3])
    return start, end


def extract_interpolated_data(start_time, end_time, y_data):
    time = [start_time, y_data[-1], end_time]
    f_inter = interpolate.PchipInterpolator(np.array(time), np.array(y_data[:3]))
    x_inter_np = np.linspace(start_time, end_time, num=int(end_time + 1), endpoint=True)
    y_inter = list(f_inter(x_inter_np))
    x_inter = list(x_inter_np)
    lst_input = countList(x_inter, y_inter)
    lst_input_str = list(map(str, lst_input))  # 다시 문자열로 변환
    df_inter = pd.DataFrame({'Time_': x_inter, 'Value': y_inter})
    return lst_input_str, df_inter
