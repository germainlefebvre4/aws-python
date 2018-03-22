#!/usr/bin/python2

import boto3

region = "eu-central-1"


ec2client = boto3.client('ec2', region_name=region)
ec2 = boto3.resource('ec2', region_name=region)

print("-----")

# Working
#services = [a for a in dir(ec2client) if 'describe' in a ]
#print "\n".join(services)
#service = services[41]
#print service
#exec("entity = ec2client." + service + "()")
#print entity

# During
services = ["instances","internet_gateways","key_pairs","network_acls","network_interfaces","placement_groups","route_tables","security_groups","subnets","volumes","vpcs"]
service = services[0]
for service in services:
  print("- %s" % (service))
  exec("entities = ec2." + service + ".all()")
  for entity in entities:
    #print dir(entity)
    #if 'id' in entity.keys():
    if hasattr(entity,'id'):
      print entity.id
    elif hasattr(entity,'name'):
      print entity.name

print("------")
subnets = ec2client.describe_subnets()
dir(subnets)
for subnet in subnets['Subnets']:
  print subnet['SubnetId']

vpcs = ec2client.describe_vpcs()
for vpc in vpcs['Vpcs']:
  print vpc['VpcId']
