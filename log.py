import os
import csv
from datetime import datetime
from main import config

# 定义日志文件路径
LOG_FILE = config["log_file"]

def get_last_token_sum(log_file):
    """
    Read CSV file and return last token
    """
    try:
        with open(log_file, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            # read all lines to list
            rows = list(reader)
            # ensure the file have at least two rows(header and at least one recording)
            if len(rows) > 1:
                last_row = rows[-1]  # get the last row
                token_sum = last_row[5]  # get the 5th item of the last row(last token)
                return token_sum
            else:
                return 0
    except FileNotFoundError:
        return "Log file missing。"
    except Exception as e:
        return f"Error: {e}"

def log_to_csv(send_time, question, image_path, response, token_count):
    """
    Save logs including calling time, question, image path, response from GPT and token count.
    """

    # initialize CSV file(if not exist create file and add header)
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["send_time", "question", "image_url", "reply", "token_count", "token_sum", "reply time"])

    reply_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 记录日志生成时间

    # write log
    with open(LOG_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        token_sum = int(get_last_token_sum(LOG_FILE)) + token_count
        writer.writerow([send_time, question, image_path, response, token_count, token_sum, reply_time])

def save_result(image_path, response):
    path = config["result_file"]

    # initialize CSV file(if not exist create file and add header)
    if not os.path.exists(LOG_FILE):
        with open(path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["id","fork","door","door_dir","door_dis","door_open","robot","robot_dir","robot_dis","AR_single","AR_multi","AR_dir","obs","obs_name","obs_dir","obs_dis","can_pass"])
    with open(path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        response = response.strip().split('|')
        writer.writerow([image_path] + response)
