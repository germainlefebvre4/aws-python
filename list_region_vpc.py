#!/usr/bin/python2
# Tested versions:
#   - Python 2.7.5
#   - Boto3 1.4.6


import sys
import time
import argparse
import boto3
from boto3.session import Session
from botocore.exceptions import ClientError

# Global variables
regions = []

# Arguments Parser
parser = argparse.ArgumentParser()
parser.add_argument('--check',
                    default=False,
                    action='store_true',
                    help="Dry run")
args = parser.parse_args()

# List regions (available trough API)
session = boto3.Session(profile_name='default')
regions = session.get_available_regions(service_name='ec2')
del session

# Show global informations
# Title
print("+-------------------------------------------+")
print("|    List non default VPCs and Instances    |")
print("|      for all regions with its owner.      |")
print("+-------------------------------------------+")

# Check mode
print("Regions: %s" % ', '.join(regions))
if args.check:
  print("Check mode: True")
print("")


for region_name in regions:

  # Region
  print("Region: %s" % region_name)
  
  ec2r = boto3.resource('ec2', region_name=region_name)
  trailc = boto3.client('cloudtrail', region_name=region_name)

  # Vpc
  for vpc in ec2r.vpcs.all():
    if not vpc.is_default:
      # Last trace 
      owner = trailc.lookup_events(LookupAttributes=[{'AttributeKey': 'EventName', 'AttributeValue': 'CreateVpc'}, {'AttributeKey': 'ResourceName', 'AttributeValue': vpc.vpc_id}])['Events'][0]['Username']
      print vpc.vpc_id, owner

  # Instances
  for inst in ec2r.instances.all():
    if inst.state['Name'] not in ["shutting-down", "terminated"]:
      owner = trailc.lookup_events(LookupAttributes=[{'AttributeKey': 'EventName', 'AttributeValue': 'RunInstances'}, {'AttributeKey': 'ResourceName', 'AttributeValue': inst.id}])['Events'][0]['Username']
      print inst.id, owner

  del trailc
  del ec2r


