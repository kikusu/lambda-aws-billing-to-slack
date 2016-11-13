# lambda-aws-billing-to-slack

Notify aws billing to slack every day(JST 12:00). 

## required
- ansible >= 2.2.0.0

## config
- put your slack webhook config file in S3

`config file`
```json
{"url":"https://<your incoming webhook>"}
```

- edit `src/lambda_function.py`

```python
boto_s3 = boto3.resource("s3")
obj = boto_s3.Object("<your bucket>", "<your config file path>")
slack_url = json.load(obj.get()["Body"])["url"]
```

## deploy
```bash
$ ansible-playbook deploy.yml --ask-vault-pass
```

```
# with AWS Config environment variable
$ AWS_PROFILE=kikusu AWS_DEFAULT_REGION=us-west-2 ansible-playbook deploy.yml
```
