#!/usr/bin/python2
# Tested versions:
#   - Python 3.4
#   - Boto3 1.7.40

import sys
import time
import argparse
import boto3
from boto3.session import Session
from botocore.exceptions import ClientError

# Arguments Parser
parser = argparse.ArgumentParser()
parser.add_argument('--check',
                    default=False,
                    action='store_true',
                    help="Dry run")
parser.add_argument('--region_name',
                    required=False,
                    help="Region Name")
args = parser.parse_args()


# Ensure region_name is defined
region_name = None
session = boto3.Session(profile_name='default')
if session.region_name is not None:
  region_name = session.region_name
del session
if args.region_name is not None:
  region_name = args.region_name

# Throw error if region_name is not defined
if region_name is None:
  print("Region is not defnied. You can define it in :")
  print(" - Arguments ")
  print(" - File ~/.aws/config ([default] section)")
  sys.exit(1)


# Show global informations
# Title
print("+----------------------------+")
print("|    List Resource Groups    |")
print("|         resources          |")
print("+---------------------------+")
# Region
print("Region: %s" % region_name)
# Check mode
if args.check:
  print("Check mode: True")
print("")


ec2r = boto3.resource('ec2', region_name=region_name)
regc = boto3.client('resource-groups', region_name=region_name)

groups = regc.list_groups().get('Groups')
for group in groups:
    group_name = group['Name']
    print(group_name)
    rescs = regc.list_group_resources(GroupName=group_name).get('ResourceIdentifiers')
    if len(rescs) > 0:
        for resc in rescs:
            print(resc)
  

