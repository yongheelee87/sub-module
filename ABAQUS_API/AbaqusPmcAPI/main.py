import configparser
from Lib.DataProcess.InputProcess import *

DEFAULT_PATH = os.getcwd()
upper_path = os.path.abspath(os.path.join(DEFAULT_PATH, os.pardir))
properties = configparser.ConfigParser()  ## 클래스 객체 생성
properties.read(os.path.join(upper_path, 'config.ini'), encoding="UTF-8")  ## 파일 읽기

aba_env = properties["ENV"] ## 섹션 선택

ABAQUS_FILE_PATH = to_raw(aba_env['inp_path'])  # inp파일 있는 경로 설정
INPUT_FILES = [file.replace('.inp', '') for file in os.listdir(ABAQUS_FILE_PATH) if '.inp' in file and 'Result' not in file]
CPU_NUM = int(aba_env['cpu'])  # Abaqus 실행 시 CPU 갯수 설정

RESULT_PATH = to_raw(ABAQUS_FILE_PATH) + '\\' + 'Result'
CRITERIA_50 = 48/1000

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    logging_initialize()

    logging_print('[INFO] Current Project Abaqus File Path: {}\n'.format(ABAQUS_FILE_PATH))
    logging_print('[INFO] Current Project Abaqus Input File: {}\n'.format(INPUT_FILES))

    isdir_and_make(RESULT_PATH)

    data_total_max = []

    for input_file in INPUT_FILES:
        run_obd_cmd = 'echo y|abaqus j={} cpus={} int'.format(input_file, str(CPU_NUM))
        # run_command_os(file_path=to_raw(ABAQUS_FILE_PATH), cmd=run_obd_cmd)   # Abaqus ODB 생성

        modify_macros_py_code(file_path=to_raw(ABAQUS_FILE_PATH), input_file=input_file)  # Abaqus Macros Python 코드 수정
        run_command_os(file_path=os.path.join(DEFAULT_PATH, 'Lib', 'AbaqusPy'), cmd='abaqus cae noGUI=abaqusMacros.py')  # Abaqus ODB를 이용하여 데이터 추출

        df_loding_pt1 = convert_csv_dataframe(to_raw(ABAQUS_FILE_PATH) + "\\" + "Result" + "\\" + input_file + "_loading_pt.csv", col=['Time', 'Stress'])
        df_pt1 = convert_csv_dataframe(to_raw(ABAQUS_FILE_PATH) + "\\" + "Result" + "\\" + input_file + "_pt1.csv", col=['Time', 'Stress'])
        df_K = convert_csv_dataframe(to_raw(ABAQUS_FILE_PATH) + "\\" + "Result" + "\\" + input_file + "_K.csv",  col=['Time', 'Energy'])

        df_loding_pt1.to_csv(to_raw(ABAQUS_FILE_PATH) + "\\" + "Result" + "\\" + input_file + "_loading_pt.csv", index=False)
        df_pt1.to_csv(to_raw(ABAQUS_FILE_PATH) + "\\" + "Result" + "\\" + input_file + "_pt1.csv", index=False)
        df_K.to_csv(to_raw(ABAQUS_FILE_PATH) + "\\" + "Result" + "\\" + input_file + "_K.csv", index=False)

        time_50 = df_pt1[df_pt1['Stress'] >= CRITERIA_50].iloc[0, 0]
        df_K['Time_50'] = df_K['Time'] - time_50
        energy = df_K[df_K['Time_50'] >= 0].iloc[0, 1]
        data_max = [input_file, df_pt1['Stress'].max(), time_50, energy]

        data_total_max.append(data_max)
    df_max = pd.DataFrame(data_total_max, columns=['Name', 'Max', 'Time_50', 'Energy'])
    df_max.to_csv(to_raw(ABAQUS_FILE_PATH) + "\\" + "Result" + "\\" + "Total_Result.csv", index=False)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
