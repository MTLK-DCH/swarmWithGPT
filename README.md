# Swarm With GPT

## Program Structure

Whole project contains: dataset folder(dataset), result folder(result_images), configuration file(config.yaml), main program(main.py), log program(log.py), data processing methods(data_processing.py).

The program will load configurations from config.yaml. Build request in main.py then save the result in log.py.

After experiment you can process the data in data_processing.py

## How to Use

1. Set your ChatGPT secret key into config.yaml
2. Set image folder path into config.yaml, ensure no other files or folders in that folder
3. Set tags file into config.yaml. tags file should have the same format as sample.(ensure sort columns as same as questions and have headers)
4. Create sys_message file and set sys_message file path into config.yaml to tell gpt its role and your requirements for it
5. Create questions file and set path into config.yaml. Ensure you have same structure as sample
6. Set GPT parameters into config.yaml
7. run main.py and get reply
