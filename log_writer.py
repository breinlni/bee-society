import time
import os


def write_new_log(logdir='./logs', temp_log_path='./temp_log.txt'):
    current_date = time.strftime("%d_%m_%Y")
    current_time = time.strftime("%H_%M_%S")
    filename = f'BeeSociety_{current_time}.txt'
    dir_path = f'{logdir}/{current_date}'
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    with open(f'{dir_path}/{filename}', 'a') as target_file, open(temp_log_path, 'r') as source_file:
        for line in source_file:
            target_file.write(line)


def write_temp_log(content, temp_log_path='./temp_log.txt'):
    with open(temp_log_path, 'a') as f:
        f.write(f'{content}\n')


def close_temp_log(temp_log_path='./temp_log.txt'):
    os.remove(temp_log_path)
