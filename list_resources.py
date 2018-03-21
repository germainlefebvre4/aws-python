#!/usr/bin/python2

import boto3

region = "eu-central-1"

ec2 = boto3.resource('ec2', region_name=region)
print "name id image_id vpc_id author"
cloudtrail = boto3.client('cloudtrail', region_name=region)
for instance in ec2.instances.all():
  for tag in instance.tags:
    if tag["Key"] == "Name":
      instance_name = tag["Value"]
  events_dict = cloudtrail.lookup_events(LookupAttributes=[{'AttributeKey':'ResourceName', 'AttributeValue':instance.id}])
  instance_author = events_dict['Events'][0]['Username']
  print instance_name, instance.id, instance.image_id, instance.vpc_id, instance_author
