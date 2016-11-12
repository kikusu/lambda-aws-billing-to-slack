# lambda-notify-slack-of-aws-billing

Notify aws billing to slack every day(JST 12:00). 

## required
- ansible >= 2.2.0.0

## config
### slack incoming webhook
- delete `group_vars/all/vault.yml`
- edit `group_vars/all/vars.yml`
```yaml
slack_url: <your slack incoming webhook>
```

## deploy
```bash
$ ansible-playbook deploy.yml --ask-vault-pass
```

```
# with AWS Config environment variable
$ AWS_PROFILE=kikusu AWS_DEFAULT_REGION=us-west-2 ansible-playbook deploy.yml
```
