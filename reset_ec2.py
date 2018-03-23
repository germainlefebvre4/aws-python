#!/usr/bin/python2

import boto3

region = "eu-central-1"

print("- List all Applicaiton Autoscaling")
#appautoscalingClient = boto3.client('application-autoscaling', region_name=region)
#appautoscaling = boto3.resource('application-autoscaling', region_name=region)

print("- List all Autoscaling")
#autoscalingClient = boto3.client('autoscaling', region_name=region)


print("- List all ELB")
elbClient = boto3.client('elb', region_name=region)
bals = elbClient.describe_load_balancers()
if len(bals["LoadBalancerDescriptions"]) > 0:
  for elb in bals["LoadBalancerDescriptions"]:
    print elb['DNSName']

print("- List all ELB v2")
elbv2Client = boto3.client('elbv2', region_name=region)
bals = elbv2Client.describe_load_balancers()
if len(bals["LoadBalancers"]) > 0:
  for elb in bals["LoadBalancers"]:
    print elb['DNSName']

print("- List all EC2")
ec2Client = boto3.client('ec2', region_name=region)
ec2 = boto3.resource('ec2', region_name=region)
for instance in ec2.instances.all():
  print instance.id

print("- List all Subnets")
subnets = ec2client.describe_subnets()
for subnet in subnets['Subnets']:
  print subnet['SubnetId']

print("- List all VPCs")
vpcs = ec2client.describe_vpcs()
for vpc in vpcs['Vpcs']:
  print vpc['VpcId']

