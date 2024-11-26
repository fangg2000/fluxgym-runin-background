This is a file that can run in the background for fluxgym. The operation is very simple. . .

1. Put the lora image you want to fine-tune in file A. A file must add a content.txt file (specifically specify the associated words corresponding to the image name), the format is such as: xxx#smile, and then put it in datasets;
2. Execute prepare.py, the command is such as: python prepare.py --name A --model 0 --vram 20, where name corresponds to the file name of all your images, the value of model 0, 1, 2 corresponds to the selected model of the original project, such as 0 corresponds to flux-dev, the value of vram corresponds to the video memory size, the default is 12G, model and vram can also be not added;
3. Execute train_test.py, the command is such as: python train_test.py --name A

Thanks to cocktailpeanut and other big guys, fluxgym is indeed a very good project.

https://github.com/cocktailpeanut/fluxgym
