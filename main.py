import base64
from openai import OpenAI
from datetime import datetime
import csv
import os

import log
from log import save_result

import yaml

# load configs
with open('config.yaml', 'r') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

client = OpenAI()

# set API secrit keys
api_key = config["api_key"]

# set headers
headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json',
}

# set questions file
questions_file = config["questions_file"]


# questions, request

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def get_questions(questions_file):
    """read csv file and build them as a dictionary"""
    result_dicts = []

    try:
        with open(questions_file, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)

            for row in reader:
                if len(row) == 2:  # ensure all rows contains two items
                    question = row[0]
                    requirement = row[1]
                    result_dicts.append({"type": "text", "text": question + requirement})

        return result_dicts

    except FileNotFoundError:
        return "File not found。"
    except Exception as e:
        return f"Error: {e}"


def ask_gpt(image_path, questions_file):
    """
    image_path: image path
    questions_file: questions file path
    This function is to ask questions to GPT for one image. It will return a string that GPT replies the questions.
    """

    # GPT API can not receive an image so here is to encode image to base64 string
    # methods getting by OpenAI CookBook: https://cookbook.openai.com/examples/multimodal/using_gpt4_vision_with_function_calling
    base64_image = encode_image(image_path)

    # get time to write log
    send_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # get string from sys_message file to tell gpt its role and your requirements for it
    with open(config["sys_message"], 'r', encoding='utf-8') as file:
        sys_message = file.read().strip()

    # prepare for the message
    system_message = {
        "role": "system",
        "content": sys_message
    }

    # Add image to message
    image_message = {
        "type": "image_url",
        "image_url": {
            "url": f"data:image/jpeg;base64,{base64_image}"
        },
    }

    # read questions from questions file
    questions = get_questions(questions_file)

    # build whole message
    my_messages = (
            [system_message] + [{
        "role": "user",
        "content": questions + [image_message]
    }]
    )

    response = client.chat.completions.create(
        model=config["gpt_p"]["model"],
        temperature=config["gpt_p"]["temperature"],
        seed=config["gpt_p"]["seed"],
        messages=my_messages,
    )

    # Observation window: to look what is the response or other, not necessary.
    # print(response)
    # print(my_messages)
    # print(len(base64_image))

    # write the log
    answer = response.choices[0].message.content
    token_count = response.usage.total_tokens
    log.log_to_csv(send_time=send_time, question=questions, image_path=image_path, response=answer,
                   token_count=token_count)

    return answer


# get dataset
folder_path = config["dataset"]
image_paths = os.listdir(folder_path)

# batch processing
# for image_path in image_paths:
#     if image_path.endswith(".jpg"):
#         path = folder_path + "/" + image_path
#
#         print(path)
#         # ask gpt for the image and save the result
#         result = ask_gpt(path, questions_file)
#         print(result)
#         save_result(image_path, result)

# for test only one image
ask_gpt("images/001.jpg", questions_file)
