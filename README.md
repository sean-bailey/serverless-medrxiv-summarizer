# serverless-medrxiv-summarizer
This project will contain the code and instructions for producing a [Serverless Machine Learning Summarization engine leveraging Python, Huggingface Transformers and AWS.](https://medium.com/p/849921f5f558)

QuickStart:

1) Download or clone this repository locally
2) `cd` to the `serverless-medrxiv-summarizer` directory
3) run `pip3 install -r requirements.txt`
4) Pick out a model at HuggingFace. For this repo, summarization models work.
5) run `python3 savemodel.py downloadAndSaveModel --transformername <model from HuggingFace>`
   1) It will download and save the model and the tokenizer inside a directory named after the model.
   2) You will have `model` and `tokenizer` subdirectories inside of it.
6) `cd` into `better-medrxiv-bot/bot-internals/terraform` and modify `main.tf` to meet your AWS requirements
   1) Focus on the vpc id and the profile.
7) Run `terraform init` and then `terraform apply`
8) Once done, `cd..` and modify `efsync.yaml` to match the outputs of both your model download script and the EFS / Subnets your Terraform used.
9) 
