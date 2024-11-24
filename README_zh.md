这是对fluxgym可在后台运行的文件，操作很简单。。。

1、把你要微调的lora图片放在文件侠A里面，A文件侠里面一定要加一个content.txt文件（专门指定图片名称对应的关联词语），格式如：xxx#smile，然后放到datasets里面；
2、执行prepare.py，命令如：python prepare.py --name A --model 0 --vram 20，其中name对应你图片所有的文件侠名称，model的值0、1、2对应原项目的选择模型，如0对应flux-dev，vram的值对应显存大小，默认12G，model和vram也可以不加；
3、执行train_test.py，命令如：python train_test.py --name A

感谢cocktailpeanut等大佬，fluxgym的确是一个很好的项目。
