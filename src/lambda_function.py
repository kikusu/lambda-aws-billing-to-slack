# coding:utf-8
import datetime
import json
import sys

import boto3

sys.path.append("./site-packages")


def lambda_handler(event, context):
    """ Lambda Handler

    :param event:
    :param context:
"""

    import pytz
    import slackweb

    del context, event

    boto_s3 = boto3.resource("s3")
    obj = boto_s3.Object("kikusu-config", "slack/kikusu-incoming-webhook.json")
    slack_url = json.load(obj.get()["Body"])["url"]

    end = datetime.datetime.now(pytz.utc)
    start = end - datetime.timedelta(days=2)

    cloudwatch = boto3.resource("cloudwatch", region_name="us-east-1")
    metric = cloudwatch.Metric("AWS/Billing", "EstimatedCharges")

    def get_metrics(service_name=None):
        dimensions = [{u'Name': 'Currency', u'Value': 'USD'}]

        if service_name is not None:
            dimensions.append({u"Name": "ServiceName", u"Value": service_name})

        data = metric.get_statistics(
            Dimensions=dimensions,
            StartTime=start,
            EndTime=end,
            Period=60 * 60 * 24,
            Statistics=["Maximum"]
        )

        result = sorted(data["Datapoints"], key=lambda x: x["Timestamp"])
        diff = result[1]["Maximum"] - result[0]["Maximum"]
        now = result[1]["Maximum"]

        return "${} (+ ${})".format(now, diff)

    slack = slackweb.Slack(slack_url)
    slack.notify(
        attachments=[
            dict(
                title="AWS Billing @ {}".format(
                    end.astimezone(pytz.timezone('Asia/Tokyo')).strftime(
                        "%Y-%m-%dT%H:%M:%S")),
                fields=[
                    dict(title="Sum",
                         value=get_metrics()),
                    dict(title="EC2",
                         value=get_metrics("AmazonEC2"),
                         short=True)
                ],
                color="good"),
        ],
        icon_emoji=":moneybag:"
    )
