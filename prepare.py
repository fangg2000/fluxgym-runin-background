import argparse
import os
import time
import math
import shutil

def initImgData(name):
    img_file_name_list = []
    content_dict = {}

    with open(f"datasets/{name}/content.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()

        for txt in lines:
            if len(txt.strip()) > 0 and "#" in txt:
                tmpArr = txt.strip().split('#')
                content_dict[tmpArr[0]] = tmpArr[1]

        shutil.copy2(f"datasets/{name}/content.txt", f"outputs/{name}/content_bak.txt")
        os.remove(f"datasets/{name}/content.txt")

    # print(content_dict)

    # 图片文件
    for fileName in os.scandir(f"datasets/{name}"):
        if fileName.is_file():
            if fileName.path.endswith(".png") or fileName.path.endswith(".jpg"):
                # print(fileName.path)
                # img_file_name_list.append(fileName.name)

                img_name = fileName.name.replace(".png", "").replace(".jpg", "")

                if img_name in content_dict:
                    # print(content_dict[img_name])
                    with open(f"datasets/{name}/{img_name}.txt", 'w', encoding='utf-8') as file:
                        file.write(f"{name},{content_dict[img_name]}")
                else:
                    # print(f"{img_name}没有对应的文本内容")
                    with open(f"datasets/{name}/{img_name}.txt", 'w', encoding='utf-8') as file:
                        file.write(name)

    pass


def initParamData(name:str, model: int, vram: int):
    #
    os.makedirs(f"outputs/{name}", exist_ok=True)
    current_path = os.getcwd()

    # 初始化--dataset.toml
    with open("outputs/mylora/dataset.toml", "r", encoding="utf-8") as f:
        lines = f.readlines()
        dataset_content = ""
        for txt in lines:
            dataset_content = dataset_content + txt.replace("mylora", name).replace("/home/fangg/other/tts/fluxgym", current_path)

        with open(f"outputs/{name}/dataset.toml", 'w', encoding='utf-8') as file:
            file.write(dataset_content)

    # 记录输入参数
    param_json = {
        'name': name,
        'model': model,
        'vram': vram,
    }

    with open(f"outputs/{name}/params.json", 'w', encoding='utf-8') as file:
        file.write(str(param_json))

    # 初始化--sample_prompts.txt
    with open("outputs/mylora/sample_prompts.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
        sample_prompts_content = ""
        for txt in lines:
            sample_prompts_content = sample_prompts_content + txt.replace("mylora", name)

        with open(f"outputs/{name}/sample_prompts.txt", 'w', encoding='utf-8') as file:
            file.write(sample_prompts_content)

    train_name = 'train_12'

    if vram == 20:
        train_name = 'train_20'
    elif vram == 16:
        train_name = 'train_16'

    # 初始化--train.sh
    with open(f"outputs/mylora/{train_name}.sh", "r", encoding="utf-8") as f:
        lines = f.readlines()
        train_content = ""
        flux_name = "bdsqlsz/flux1-dev2pro-single/flux1-dev2pro.safetensors"

        if model == 0:
            flux_name = "flux1-dev.sft"
        elif model == 1:
            flux_name = "flux1-schnell.safetensors"

        for txt in lines:
            train_content = train_content + txt.replace("mylora", name).replace("/home/fangg/other/tts/fluxgym",
                current_path).replace("mymodel", flux_name)

        with open(f"outputs/{name}/train.sh", 'w', encoding='utf-8') as file:
            file.write(train_content)

    print("数据准备完成")
    pass


def init_data(name: str, model: int, vram: int):
    print(f'准备开始处理数据...')
    # print(f'lora名称--{name}, 显存--{vram}G')

    if vram > 20:
        vram = 20
    elif vram > 16:
        vram = 16
    else:
        vram = 12

    if name == "mylora":
        print(f'名称有误')
        return

    if os.path.exists(f"datasets/{name}"):
        # 初始化图片对应文本数据
        initImgData(name)

        # 初始化参数
        initParamData(name, model, vram)
    else:
        print(f"名称对应的图片数据集不存在")














if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', type=str, default="mylora")
    parser.add_argument('--model', type=int, default=2)
    parser.add_argument('--vram', type=int, default=12)
    args = parser.parse_args()

    init_data(args.name, args.model, args.vram)