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
print("+-----------------------------------+")
print("|    Delete non default VPCs and    |")
print("|       and its sub-resources       |")
print("+-----------------------------------+")
# Region
print("Region: %s" % region_name)
# Check mode
if args.check:
    print("Check mode: True")
print("")


ec2c = boto3.client('ec2', region_name=region_name)

nats = ec2c.describe_nat_gateways().get('NatGateways')
for nat in nats:
    if nat['State'] not in ["deleting", "deleted"]:
        print nat['NatGatewayId']
        if not args.check:
            ec2c.delete_nat_gateway(NatGatewayId=nat['NatGatewayId'])



ec2r = boto3.resource('ec2', region_name=region_name)

for vpc in ec2r.vpcs.all():
    if not vpc.is_default:
        for ins in vpc.instances.all():
            print ins.instance_id
            if not args.check:
                ins.terminate()
            for vol in ins.volumes.all():
                print vol.id
                if not args.check:
                    vol.delete()
            #for snap in ec2r.snapshots.all():
            #    print snap.id
            #    snap.delete()
            #for nic_ass in vpc.network_interface_associations.all():
            #    print nic_ass
            #    nic_ass.delete()
            for nic in vpc.network_interfaces.all():
                print nic.id
                if not args.check:
                    nic.delete()
            for sub in vpc.subnets.all():
                print sub.subnet_id
                if not args.check:
                    sub.delete()
            for igw in vpc.internet_gateways.all():
                print igw.internet_gateway_id
                if not args.check:
                    igw.detach_from_vpc(VpcId=vpc.vpc_id)
                    igw.delete()
            for rtb in vpc.route_tables.all():
                for ass in rtb.associations:
                    if not ass.main:
                        if not args.check:
                            ass.delete()
                if len(rtb.associations_attribute) > 0:
                    if not rtb.associations_attribute[0]['Main']:
                        print rtb.route_table_id
                        if not args.check:
                            rtb.delete()
                if len(rtb.associations_attribute) == 0:
                    print rtb.route_table_id
                    if not args.check:
                        rtb.delete()
            for sg in vpc.security_groups.all():
                if sg.group_name != "default":
                    print sg.id
                    if not args.check:
                        sg.delete()
            for nacl in vpc.network_acls.all():
                if not nacl.is_default:
                    print nacl.id
                    if not args.check:
                        nacl.delete()

        print vpc.vpc_id
        if not args.check:
          vpc.delete()

        #for keyp in vpc.key_pairs.all():
        #    print keyp.id
        #for meta in vpc.meta.all():
        #    print meta.id
        #for plc in vpc.placement_groups.all():
        #    print plc.id
        #for vaddr in vpc.vpc_addresses.all():
        #    print vaddr.id
        #for peer in vpc.vpc_peering_connections.all():
        #    print peer.id

