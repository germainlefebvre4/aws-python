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
parser.add_argument('--group_name',
                    required=False,
                    help="Resource Group Name")
parser.add_argument('--start',
                    required=False,
                    action='store_true',
                    help="Start the Resource Group Instances")
parser.add_argument('--stop',
                    required=False,
                    action='store_true',
                    help="Stop the Resource Group Instances")
args = parser.parse_args()


# Control the arguments
if args.start and args.stop:
    print("Error: Wrong parameters.")
    print("You cannot start and stop instances at the same time.")
    sys.exit(1)
if not(args.start or args.stop):
    print("Error: Wrong parameters.")
    print("You need to perform an action on instances: start or stop.")
    sys.exit(1)


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
print("+-------------------------------+")
print("|    Start or Stop Instances    |")
print("|      from Resource Groups     |")
print("+-------------------------------+")
# Region
print("Region: %s" % region_name)
# Check mode
if args.check:
    print("Check mode: True")
print("")



# Instanciate lib
ec2r = boto3.resource('ec2', region_name=region_name)
regc = boto3.client('resource-groups', region_name=region_name)

# LIst all or single Resource Group(s) depending on parameters
if args.group_name:
    groups = regc.get_group(GroupName=args.group_name.get('Group'))
else:
    groups = regc.list_groups().get('Groups')
# Browser Resource Groups
for group in groups:
    group_name = group['Name']
    rescs = regc.list_group_resources(GroupName=group_name).get('ResourceIdentifiers')
    if len(rescs) > 0:
        for resc in rescs:
            if resc['ResourceType'] in ["AWS::EC2::Instance"]:
                inst_id = resc['ResourceArn'].split(":instance/")[1]
                inst = ec2r.Instance(inst_id)
                if args.start:
                    if not args.check:
                        inst.start()
                    action = "start"
                elif args.stop:
                    if not args.check:
                        inst.stop()
                    action = "stop"
                print(action, inst_id)
