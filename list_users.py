#!/usr/bin/python2

import boto3

iamr = boto3.resource('iam')

for u in iamr.users.all():
    #print u.name, u.arn, u.meta, u.user_name, u.user_id
    print u.user_name
