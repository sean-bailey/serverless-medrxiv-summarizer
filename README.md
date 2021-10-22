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
   3) I have found "mrm8488/roberta-med-small2roberta-med-small-finetuned-cnn_daily_mail-summarization" works well, speedwise, and is the default inside `serverless.yml`
6) `cd` into `better-medrxiv-bot/bot-internals/terraform` and modify `main.tf` to meet your AWS requirements
   1) Focus on the vpc id and the profile.
7) Run `terraform init` and then `terraform apply`
8) Once done, `cd..` and modify `efsync.yaml` to match the outputs of both your model download script and the EFS / Subnets your Terraform used.
9) Next, run `efsync2 -cf efsync.yaml` and let the upload complete. This can take a few minutes. [In the meantime, check out efsync2 for more info!](https://github.com/sean-bailey/efsync2)
10) From the output of that last command, head into `/better-medrxiv-bot/bot-internals/medrxiv-summarizer/serverless.yml` and modify the security groups and subnet ids appropriately.
    1) Make sure `MAIN_DIR` is set to the same base directory name of the model you downloaded in 5.
11) Run `serverless deploy -c serverless.yml`, and let it finish.
12) Head over to Lambda, find your function as named in your `serverless.yml`, and test it out! 

Here is a good test event for Lambda:
```
{
  "body": {
    "url": "https://www.medrxiv.org/content/10.1101/2021.10.04.21264434v1"
  }
}
```

You may notice the first test takes upwards of 15 seconds to run, but subsequent tests can complete in less than 5 seconds. This is due to Lambda cold starting, and can be mitigated with reserved concurrency if you'd prefer. For this tutorial, I found it as an unnecessary expense.

Head over to API Gateway next, and select the API related to your function. Head to the `POST`, and click the TEST lightning bolt.

Try using this as your Request Body
```
{
    "url": "https://www.medrxiv.org/content/10.1101/2021.10.04.21264434v1"
}

```

You'll probably see that the first time may fail. Try running it again afterwards and it will work fine. API Gateway has a timeout of 29 seconds, so it will timeout before the cold-started lambda completes.


Open up the `get_summarized_url.html` file in the `bot-internals` folder.
change this line: 
`const APIGatewayUrl="<your-api-gateway-url>"`
to match your API Gateway URL endpoint, which is provided by the output from Serverless.

Create an S3 static site, and use this file as your index. Visit it, and see your serverless Machine Learning Inference system in action!


# <a name="connect"></a> 🔗 Connect with me

<a href="https://blog.baileytec.net" target="_blank"><img alt="Personal Website" src="https://img.shields.io/badge/Personal%20Website-%2312100E.svg?&style=for-the-badge&logoColor=white" /></a>
<a href="https://twitter.com/seanbailey518" target="_blank"><img alt="Twitter" src="https://img.shields.io/badge/twitter-%231DA1F2.svg?&style=for-the-badge&logo=twitter&logoColor=white" /></a>
<a href="https://medium.com/@seanbailey518" target="_blank"><img alt="Medium" src="https://img.shields.io/badge/medium-%2312100E.svg?&style=for-the-badge&logo=medium&logoColor=white" /></a>
<a href="https://www.linkedin.com/in/baileytec/" target="_blank"><img alt="LinkedIn" src="https://img.shields.io/badge/linkedin-%230077B5.svg?&style=for-the-badge&logo=linkedin&logoColor=white" /></a>
