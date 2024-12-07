import os
import sys
os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "1"
os.environ['GRADIO_ANALYTICS_ENABLED'] = '0'
sys.path.insert(0, os.getcwd())
sys.path.append(os.path.join(os.path.dirname(__file__), 'sd-scripts'))
from subprocess import Popen, PIPE, STDOUT
# import subprocess
import gradio as gr
from PIL import Image
import torch
import uuid
import shutil
import json
import yaml
import argparse

from app import download as myDownload

MAX_IMAGES = 150


def myTrain(lora_name):
    if lora_name == "" or lora_name == "mylora":
        print(f"没有指定数据集名称")
        return

    if not os.path.exists(f"datasets/{lora_name}"):
        print(f"没有指定数据集名称")
        return

    base_model = "bdsqlsz/flux1-dev2pro-single"

    try:
        model_type = 2

        with open(f"outputs/{lora_name}/params.json", "r", encoding="utf-8") as f:
            lines = f.read()
            param_json = eval(lines)
            model_type = param_json['model']

        if model_type == 0:
            base_model = "flux-dev"
        elif model_type == 1:
            base_model = "flux-schnell"

        myDownload(base_model)

        custom_tc = True
        print(f"开始后台推理...")

        my_start_training(base_model, lora_name)
    except Exception as e:
        print("后台推理异常：", e)
        pass

def resolve_path_without_quotes(p):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    norm_path = os.path.normpath(os.path.join(current_dir, p))
    return norm_path

def my_start_training(base_model, lora_name):
    print("判断开始...")

    file_type = "sh"
    if sys.platform == "win32":
        file_type = "bat"

    print("判断正常a")

    sh_filename = f"train.{file_type}"
    sh_filepath = resolve_path_without_quotes(f"outputs/{lora_name}/{sh_filename}")

    print("判断正常b")

    # Train
    if sys.platform == "win32":
        command = sh_filepath
    else:
        command = f"bash \"{sh_filepath}\""

    # Use Popen to run the command and capture output in real-time
    env = os.environ.copy()
    env['PYTHONIOENCODING'] = 'utf-8'
    env['LOG_LEVEL'] = 'DEBUG'

    # result = subprocess.run(command, shell=True, capture_output=True, text=True)
    result = exec_command(command)
    # 打印命令输出结果
    print(f"结果:{result}")

def exec_command(command):
    propress = Popen(command, stdout=PIPE, stderr=STDOUT, encoding='utf-8', shell=True)
    # propress = subprocess.run(command, shell=True, capture_output=True, text=True)
    with propress.stdout:
        for line in iter(propress.stdout.readline, b''):
            if len(line) > 0:
                print(line.encode('utf-8').strip().decode('utf-8'))

    exitcode = propress.wait()
    return exitcode

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', type=str, default="mylora")
    args = parser.parse_args()

    myTrain(args.name)
