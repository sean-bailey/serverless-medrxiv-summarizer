"""

"""
import os
import fire
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

def downloadAndSaveModel(transformername,rootdir=None):
    if rootdir is None:
        rootdir="./"+transformername.replace("/","-")
    tokenizer = AutoTokenizer.from_pretrained(transformername)

    model = AutoModelForSeq2SeqLM.from_pretrained(transformername)
    tokenizerdir=rootdir+"/tokenizer"
    modeldir=rootdir+"/model"
    tokenizer.save_pretrained(tokenizerdir)
    model.save_pretrained(modeldir)
    if os.path.exists(tokenizerdir+"/tokenizer_config.json"):
        os.rename(tokenizerdir+"/tokenizer_config.json",tokenizerdir+"/config.json")

    print("Done!")
    print("Your download dir is: ")
    print(rootdir)


if __name__ == '__main__':
    fire.Fire()
