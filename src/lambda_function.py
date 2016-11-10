# coding:utf-8
import datetime
import sys

import boto3

sys.path.append("./site-packages")


def lambda_handler(event, context):
    """
    :param event:
    :param context:
    """
    import pytz
    import slackweb

    del context

    slack_url = event["slack_url"]

    end = datetime.datetime.now(pytz.utc)
    start = end - datetime.timedelta(days=2)

    cloud_watch = boto3.client("cloudwatch", region_name="us-east-1")

    def fee_format(metric):
        result = sorted(metric["Datapoints"], key=lambda x: x["Timestamp"])
        diff = result[-1]["Maximum"] - result[0]["Maximum"]
        now = result[1]["Maximum"]

        return "${} (+ ${})".format(now, diff)

    def get_metrics(service_name=None):
        dimensions = [{u'Name': 'Currency', u'Value': 'USD'}]

        if service_name is not None:
            dimensions.append({u"Name": "ServiceName", u"Value": service_name})

        return cloud_watch.get_metric_statistics(
            Dimensions=dimensions,
            Namespace="AWS/Billing",
            MetricName="EstimatedCharges",
            StartTime=start,
            EndTime=end,
            Period=60 * 60 * 24,
            Statistics=["Maximum"]
        )

    slack = slackweb.Slack(slack_url)
    slack.notify(
        attachments=[
            dict(
                title="AWS Billing @ {}".format(
                    end.astimezone(pytz.timezone('Asia/Tokyo')).strftime(
                        "%Y-%m-%dT%H:%M:%S")),
                fields=[
                    dict(title="Sum",
                         value=fee_format(get_metrics())),
                    dict(title="EC2",
                         value=fee_format(get_metrics("AmazonEC2")),
                         short=True)
                ],
                color="good"),
        ],
        icon_emoji=":moneybag:"
    )
