#!/usr/bin/python2
""" This script browse main AWS Services and delete all non-default resources"""

import sys
import time
import argparse
import boto3
#from boto3.session import Session
from botocore.exceptions import ClientError

# Arguments Parser
parser = argparse.ArgumentParser()
parser.add_argument('--check',
                    default=False,
                    action='store_true',
                    help="Dry run")
parser.add_argument('-r', '--region_name',
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
    print "Region is not defnied. You can define it in :"
    print " - Arguments "
    print " - File ~/.aws/config ([default] section)"
    sys.exit(1)


# Show global informations
# Title
print "+-----------------------------------+"
print "|       Delete all non default      |"
print "|    resources and sub-resources    |"
print "+-----------------------------------+"
# Region
print "Region: %s" % region_name
# Check mode
if args.check:
    print "Check mode: True"
print ""


# EFS
print "EFS"
efsc = boto3.client('efs', region_name=region_name)
print " Clean file systems"
fss = efsc.describe_file_systems().get('FileSystems')
for fs in fss:
    fs_id = fs.get('FileSystemId')

    # Run deleting mount targets
    mts = efsc.describe_mount_targets(FileSystemId=fs_id).get('MountTargets')
    for mt in mts:
        mt_id = mt.get('MountTargetId')
        sys.stdout.write("EFS Mount Target %s... " % mt_id)
        if not args.check:
            efsc.delete_mount_target(MountTargetId=mt_id)
        print "deleting"

    # Wait for mount targets be deleted
    mt_count = 1
    while mt_count != 0:
        time.sleep(1)
        mts = efsc.describe_mount_targets(FileSystemId=fs_id).get('MountTargets')
        mt_count = len(mts)
    print "    EFS Mount Targets %s... " % fs_id
    print "deleted"

    sys.stdout.write('    EFS %s...' % fs_id)
    if not args.check:
        efsc.delete_file_system(FileSystemId=fs_id)
    print "deleted"

    #tags = efsc.describe_tags(FileSystemId=fs_id).get('Tags')
    #for tag in tags:
    #    tag_name = tag.get('Name')
    #    sys.stdout.write('    EFS Tag %s...' % tag_name)
    #    #efsc.delete_tag(FileSystemId=fs_id, Tags[tag_name])
    #    print "deleted"


# RDS
print "RDS"
rdsc = boto3.client('rds', region_name=region_name)
rdss = rdsc.describe_db_instances().get('DBInstances')
print " Clean rds instances"
for rds in rdss:
    rds_name = rds.get('DBInstanceIdentifier')
    rds_arn = rds.get('DBInstanceArn')
    if rds.get('DBInstanceStatus') != 'deleting':
        sys.stdout.write('    RDS %s... ' % rds_name)
        if not args.check:
            rdsc.delete_db_instance(DBInstanceIdentifier=rds_name, SkipFinalSnapshot=True)
        print "deleted"
del rdsc


# Browse DynamoDB
print "DynamoDB"
ddbc = boto3.client('dynamodb', region_name=region_name)
print " Clean dynamodb tables"
ddbs = ddbc.list_tables().get('TableNames')
for ddb_name in ddbs:
    ddb = ddbc.describe_table(TableName=ddb_name).get('Table')
    print ddb
    ddb_arn = ddb.get('TableArn')
    ddb_status = ddb.get('TableStatus')
    sys.stdout.write("DynamoDB Table %s... " % ddb_name)
    if not args.check:
        ddbc.delete_table(TableName=ddb_name)
    print "deleted"


# Browse LoadBalancer items
print "Load Balancer"
elbc = boto3.client('elb', region_name=region_name)
elbs = elbc.describe_load_balancers().get('LoadBalancerDescriptions')
print " Clean load balancers"
for elb in elbs:
#    for instance in range(len(elbs[elb].get('Instances'))):
#        print " Clean instances"
#        sys.stdout.write('    Instance %s... ' % trainee["Name"])
#        instance.terminate()
#        print "deleted"
    elb_name = elb.get('LoadBalancerName')
    elb_dns = elb.get('DNSName')
    sys.stdout.write('    Load Balancer %s... ' % elb_name)
    if not args.check:
        elbc.delete_load_balancer(LoadBalancerName=elb_name)
    print "deleted"
del elbc


# Browse LoadBalancerV2 items
print "Load Balancer V2"
print " Clean load balancers"
elbv2c = boto3.client('elbv2', region_name=region_name)
elbs = elbv2c.describe_load_balancers().get('LoadBalancers')
for elb in elbs:
    elb_name = elb.get('LoadBalancerName')
    elb_arn = elb.get('LoadBalancerArn')
    elb_dns = elb.get('DNSName')

    # Listeners
    elb_lsn = elbv2c.describe_listeners(LoadBalancerArn=elb_arn).get('Listeners')
    for tg in elb_lsn:
        lsn_name = tg.get('ListenerName')
        lsn_arn = tg.get('ListenerArn')
        sys.stdout.write('     Listener %s...' % lsn_name)
        if not args.check:
            elbv2c.delete_listener(ListenerArn=lsn_arn)
        print 'deleted'

    # Target Groups
    elb_tg = elbv2c.describe_target_groups(LoadBalancerArn=elb_arn).get('TargetGroups')
    for tg in elb_tg:
        tg_name = tg.get('TargetGroupName')
        tg_arn = tg.get('TargetGroupArn')
        sys.stdout.write('     Target Group %s...' % tg_name)
        if not args.check:
            elbv2c.delete_target_group(TargetGroupArn=tg_arn)
        print 'deleted'

    sys.stdout.write('    Load Balancer %s... ' % elb_name)
    if not args.check:
        elbv2c.delete_load_balancer(LoadBalancerArn=elb_arn)
    print "deleted"

# Standalone entities
# Target Groups
tgs = elbv2c.describe_target_groups().get('TargetGroups')
for tg in tgs:
    tg_name = tg.get('TargetGroupName')
    tg_arn = tg.get('TargetGroupArn')
    sys.stdout.write('    Target Group %s...' % tg_name)
    if not args.check:
        elbv2c.delete_target_group(TargetGroupArn=tg_arn)
    print 'deleted'

del elbv2c


# Brows Auto Scaling items
print "Auto Scaling"
print " Clean auto scaling groups"
ascac = boto3.client('autoscaling', region_name=region_name)
asgs = ascac.describe_auto_scaling_groups().get('AutoScalingGroups')
for asg in asgs:
    asg_name = asg.get('AutoScalingGroupName')
    asg_arn = asg.get('AutoScalingGroupArn')
    sys.stdout.write('    Auto Scaling Group %s...' % asg_name)
    if not args.check:
        ascac.delete_auto_scaling_group(AutoScalingGroupName=asg_name, ForceDelete=True)
    print 'deleted'

print " Clean launch configuration"
ascac = boto3.client('autoscaling', region_name=region_name)
lncs = ascac.describe_launch_configurations().get('LaunchConfigurations')
for lnc in lncs:
    lnc_name = lnc.get('LaunchConfigurationName')
    lnc_arn = lnc.get('LaunchConfigurationArn')
    sys.stdout.write('    Launch Configuration %s...' % lnc_name)
    if not args.check:
        ascac.delete_launch_configuration(LaunchConfigurationName=lnc_name)
    print 'deleted'


# Browse EC2 items
print "EC2"
# ec2c
print " Clean network acls"
ec2c = boto3.client('ec2', region_name=region_name)
nacls = ec2c.describe_network_acls().get('NetworkAcls')
for nacl in nacls:
    if not nacl.get('IsDefault'):
        nacl_id = nacl.get('NetworkAclId')
        nacl_name = nacl.get('NetworkAclName')
        sys.stdout.write("Network ACL %s... " % nacl_id)
        if not args.check:
            ec2c.delete_network_acl(NetworkAclId=nacl_id)
        print "deleted"

print " Network interfaces"
nics = ec2c.describe_network_interfaces().get('NetworkInterfaces')
for nic in nics:
    print nic
    nic_id = nic.get('NetworkInterfaceId')
    #ec2c.delete_network_interface(NetworkInterfaceId=nic_id)

print " Clean instances"
reservs = ec2c.describe_instances().get('Reservations')
for reserv in reservs:
    insts = reserv.get('Instances')
    for inst in insts:
        inst_state = inst.get('State').get('Name')
        if inst_state not in    ["shutting-down", "terminated"]:
            inst_id = inst.get('InstanceId')
            # t = inst.get('Tags')
            # inst_name = [x['Value'] for x in t if x['Key'] == 'Name'][0]
            sys.stdout.write("Instance %s... " % inst_id)
            if not args.check:
                ec2c.terminate_instances(InstanceIds=[inst_id])
            print "deleted"

print " Clean security groups"
sgs = ec2c.describe_security_groups().get('SecurityGroups')
for sg in sgs:
    if not sg.get('GroupName') == "default":
        sg_id = sg.get('GroupId')
        sg_name = sg.get('GroupName')
        sys.stdout.write("Security Group %s... " % sg_id)
        if not args.check:
            ec2c.delete_security_group(GroupId=sg_id)
        print "deleted"
del sgs

print " Clean volumes"
vols = ec2c.describe_volumes().get('Volumes')
for vol in vols:
    vol_id = vol.get('VolumeId')
    vol_name = vol.get('VolumeName') if vol.get('VolumeName') else vol.get('VolumeId')
    sys.stdout.write("Volume %s... " % vol_id)
    if not args.check:
        ec2c.delete_volume(VolumeId=vol_id)
    print "deleted"
del vols

print " Clean route tables"
rtbs = ec2c.describe_route_tables().get('RouteTables')
for rtb in rtbs:
    rtb_id = rtb.get('RouteTableId')
    rtb_name = rtb.get('RouteTableName') if rtb.get('RouteTableName') else rtb.get('RouteTableId')
    if len(rtb.get('Associations')) > 0 and rtb.get('Associations'):
        if not rtb.get('Associations')[0]['Main']:
            rtba_id = rtb.get('Associations')[0].get('RouteTableAssociationId')
            sys.stdout.write("Route Association %s... " % rtba_id)
            if not args.check:
                ec2c.disassociate_route_table(AssociationId=rtba_id)
            print "disassociated"
            sys.stdout.write("Route Table %s... " % rtb_id)
            if not args.check:
                ec2c.delete_route_table(RouteTableId=rtb_id)
            print "deleted"
    elif len(rtb.get('Associations')) == 0:
        sys.stdout.write("Route Table %s... " % rtb_id)
        if not args.check:
            ec2c.delete_route_table(RouteTableId=rtb_id)
        print "deleted"
del rtbs

print " Clean subnets"
subnets = ec2c.describe_subnets().get('Subnets')
for subnet in subnets:
    if not subnet.get('DefaultForAz'):
        subnet_id = subnet.get('SubnetId')
        ec2c.delete_subnet(SubnetId=subnet_id)

print " Clean internet gateway"
igws = ec2c.describe_internet_gateways().get('InternetGateways')
for igw in igws:
    if igw.get('Attachments'):
        igw_id = igw.get('InternetGatewayId')
        vpc_id = igw.get('Attachments')[0].get('VpcId')
        vpc = ec2c.describe_vpcs(VpcIds=[vpc_id])
        if not vpc.get('Vpcs')[0].get('IsDefault'):
            sys.stdout.write("Internet Gateway %s... " % igw_id)
            if not args.check:
                ec2c.detach_internet_gateway(InternetGatewayId=igw_id, VpcId=vpc_id)
            print "detached"
            sys.stdout.write("Internet Gateway %s... " % igw_id)
            if not args.check:
                ec2c.delete_internet_gateway(InternetGatewayId=igw_id)
            print "deleted"
del igws

print " Clean vpc"
vpcs = ec2c.describe_vpcs().get('Vpcs')
for vpc in vpcs:
    if not vpc.get('IsDefault'):
        vpc_id = vpc.get('VpcId')
        sys.stdout.write("VPC %s... " % vpc_id)
        if not args.check:
            ec2c.delete_vpc(VpcId=vpc_id)
        print "deleted"


# Browse S3 Buckets
print "S3"
s3c = boto3.client("s3", region_name=region_name)
print " Clean buckets"
buckets = s3c.list_buckets().get('Buckets')
for bucket in buckets:
    bucket_name = bucket.get('Name')
    bucket_loc = s3c.get_bucket_location(Bucket=bucket_name).get('LocationConstraint')
    if bucket_loc == region_name:
        #print bucket_name
        objs = s3c.list_objects_v2(Bucket=bucket_name)
        while objs['KeyCount'] > 0:
            obj_del = [{'Key':obj['Key']} for obj in objs['Contents']]
            sys.stdout.write("S3 Bucket %s objets... " % bucket_name)
            if not args.check:
                s3c.delete_objects(Bucket=bucket_name,
                                   Delete={'Objects': obj_del})
            print "deleted"
            objs = s3c.list_objects_v2(Bucket=bucket_name)

        try:
            sys.stdout.write("S3 Bucket %s... " % bucket_name)
            if not args.check:
                s3c.delete_bucket(Bucket=bucket_name)
            print "deleted"
        except ClientError as e:
            print "error"


# Browse CloudFront
print "Cloudfront"
clfc = boto3.client('cloudfront', region_name=region_name)
print " Clean distribution"
clfs = clfc.list_distributions().get('DistributionList').get('Items')
if clfs is not None:
    for clf in clfs:
        clf_id = clf.get('Id')
        dist = clfc.get_distribution(Id=clf_id).get('Distribution')
        dist_conf = clfc.get_distribution_config(Id=clf_id)
        #print clf
        #print dist
        #print dist_conf
        clf_conf = dist_conf.get('DistributionConfig')
        clf_etag = dist_conf.get('ETag')

        if not args.check:
            if clf_conf['Enabled']:
                clf_conf['Enabled'] = False
                sys.stdout.write("Distribution %s... " % clf_id)
                if not args.check:
                    clfc.update_distribution(Id=clf_id, IfMatch=clf_etag,
                                             DistributionConfig=clf_conf)
                print "disabling"
            print "(The following step might take time... long time...)"
            sys.stdout.write("Distribution %s... " % clf_id)
            clf_status = 'InProgress'
            while clf_status == 'InProgress':
                time.sleep(5)
                clf_status = clfc.get_distribution(Id=clf_id).get('Distribution')['Status']
                #print " ...%s" % clf_status
            print "disabled"

        sys.stdout.write("Distribution %s... " % clf_id)
        if not args.check:
            clfc.delete_distribution(Id=clf_id, IfMatch=clf_etag)
        print "deleted"
