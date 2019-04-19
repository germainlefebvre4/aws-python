#!/usr/bin/env python
# Author: Germain LEFEBVRE [Ineat]

# Prerequisites
#   01 - Create API Access Key in AWS Accounts to monitor
#   02 - Fill ~/.aws/credentials with API Access Keys
#   03 - Fill ./config.yml 'aws_account' dict with aws profiles as following
#        aws_accounts:
#          - name: Ineat iLab
#            profile: INEAT_ILAB

#   04 - Create InfluxDB database 'aws'
#       $ influx -execute 'create databases aws'
#   05 - Run the python script
#   06 - Stalk your AWS billing costs in Grafana

from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import yaml
import boto3
from influxdb import InfluxDBClient



# Force region to work
REGION_NAME = "eu-west-1"

# AWS type cost
AWS_COST_TYPE = ['UnblendedCost']

# Load configuration file
with open("config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.SafeLoader)

# InfluxDB connexion
inf_cl = InfluxDBClient('localhost', 8086, '', '', 'aws')


# Browse AWS Accounts Profiles
# Located in ~/.aws/credentials
for account in cfg['aws_accounts']:
    print(account['name'])

    # Open AWS Cost Explore
    # When use Profile or Access Key
    if 'profile' in account.keys():
        session = boto3.Session(region_name=REGION_NAME,
                                profile_name=account['profile'])
    elif 'access_key' in account.keys():
        session = boto3.Session(region_name=REGION_NAME,
                                aws_access_key_id=account['access_key'],
                                aws_secret_access_key=account['secret_key'])

    aws_cl_ce = session.client('ce')

    # Load Costs dataset
    cost_usage = aws_cl_ce.get_cost_and_usage(
        TimePeriod={
            #'Start': (date.today() + relativedelta(days=-1)).strftime('%Y-%m-%d'),
            'Start': (date.today() + relativedelta(months=-1)).strftime('%Y-%m-01'),
            'End': (date.today() + relativedelta(months=+1)).strftime('%Y-%m-01'),
        },
        Granularity='MONTHLY',
        Metrics=[
            ",".join(AWS_COST_TYPE)
        ]
    )

    # Print dateset
    for cost_type in AWS_COST_TYPE:
        for metric in cost_usage['ResultsByTime']:
            account_name = account['name']
            metric_time_type = "monthly"
            metric_start = metric['TimePeriod']['Start']
            metric_amount = metric['Total'][cost_type]['Amount']
            metric_unit = metric['Total'][cost_type]['Unit']
            print("%s %s %s" % (metric_start, metric_amount, metric_unit))

            json_body = [
                {
                    "measurement": "billing",
                    "tags": {
                        "account": account_name,
                        "time type": metric_time_type,
                    },
                    #"time": datetime.now().isoformat(),
                    "time": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
                    "fields": {
                        "value": metric['Total'][cost_type]['Amount']
                    }
                }
            ]
            inf_cl.write_points(json_body)

#result = inf_cl.query('select value from billing;')
#print("Result: {0}".format(result))
