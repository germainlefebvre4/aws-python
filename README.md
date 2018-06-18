# AWS SDK Python scripts

Some useful scripts to list or clean entire environments.

**Table of Contents**
1. [Requirements](#requirements)
2. [AWS Configuration](#aws-configuration)
   1. [Create an Access Key](#create-an-access-key)
   2. [Configure credentials](#configure-credentials)
      1. [Guided configuration](#guided-configuration)
      2. [Manual configuration](#manual-configuration)
3. [Running the scripts](#running-the-scripts)
   1. [Delete VPCs resources](#delete-vpcs-resources)
      1. [Description](#description)
      2. [Usage](#usage)
      3. [Examples](#examples)
   2. [List resources with their owner](#list-resources-with-their-owner)
      1. [Description](#description)
      2. [Usage](#usage)
      3. [Examples](#examples)
   3. [Delete Main AWS Services from Region](#delete-main-aws-services-from-region)
      1. [Description](#description)
      2. [Usage](#usage)
      3. [Examples](#examples)

## Requirements
These scripts depends on `boto3` package, the AWS SDK for Python and require Python 2.6+.
You can install `boto3`using yum
```bash
$ yum install python2-boto3
```
or using pip
```bash
$ pip install boto3
```

## AWS configuration

### Create an Access Key
To use AWS API calls you need to make your account reachable with an Access Account. 

See the [Security Credentials](http://aws.amazon.com/security-credentials) page for more information on getting your keys. For more information on configuring boto3, check out the Quickstart section in the [developer guide](https://boto3.readthedocs.org/en/latest/guide/quickstart.html).

### Configure credentials
You need to set up your AWS security credentials previously created to allow the API calls.

#### Guided configuration
You can use the AWS CLI to configure aws credentials. In that case you need to install the `awscli` with yum
```bash
$ yum install -y awscli
```
or pip
```bash
$ pip install awscli --upgrade --user
```

Now run `aws configure` and fill the fields `ACCESS_KEY`, `SECRET`and `REGION`.
```bash
$ aws configure
```

Your aws profile is ready.

#### Manual configuration
On Linux environments fill the configuration file at `~/.aws/credentials` with your credentials previously made :
```bash
$ vi ~/.aws/credentials
```
```ini
[default]
aws_access_key_id = <your access key id>
aws_secret_access_key = <your secret key>
```

(optionnal) You can also fill the `~/.aws/config` file to set your region on default profile
```bash
$ vi ~/.aws/config
```
```ini
[default]
region = <your aws region> # e.g. region = eu-central-1
```

Your aws profile is ready.


## Running the scripts

### Delete VPCs resources
**Beware!** *You need to provide AWS Access Key with high rights elevation.*

#### Description
Name: `delete_vpcs.py`
Description: Clear non-default resources on the region (from your profile or in parameter of the script).
Technical: This script mainly uses `boto3.resource` class to instanciate AWS entities.
Parameters:
* `--check` : (none) Enable check mode and do not apply deletions
* `--region_name <region>` : (string) Name of the (only one) AWS Region (e.g. eu-west-1, eu-central-1)

#### Usage
```bash
$ ./delete_vpcs.py
```
```
+-----------------------------------+
|    Delete non default VPCs and    |
|       and its sub-resources       |
+-----------------------------------+
```

#### Examples

Show some help on usage
```bash
$ ./delete_vpcs.py -h
```

Run on Dry Run
```bash
$ ./delete_vpcs.py --check
```

Run on a specific region (parameter override profile)
```bash
$ ./delete_vpcs.py --region_name=eu-central-1
```


### List resources with their owner

#### Description
Name: `list_region_vpc.py`
Description: List non-default VPCs and instances (for the moment) with their creator in order to trace who created it.
Technical: This script mainly uses `boto3.resource` class to instanciate AWS entities.
Parameters:
* `--check` : (none) Enable check mode and do not apply any action [implemented but not used yet]

#### Usage
```bash
$ ./list_region_vpc.py
```
```
+-------------------------------------------+
|    List non default VPCs and Instances    |
|      for all regions with its owner.      |
+-------------------------------------------+
```

#### Examples

Show some help
```bash
$ ./list_region_vpc.py -h
```


### Delete Main AWS Services from Region

#### Description
Name: `reset_region.py`
Description: Browse and delete main AWS Service non-default resources.
Technical: This script mainly uses `boto3.client` class to instanciate AWS entities.
Parameters:
* `--check` : (none) Enable check mode and do not apply any action [implemented but not used yet]
* `--region_name <region>` : (string) Name of the (only one) AWS Region (e.g. eu-west-1, eu-central-1)

#### Usage
```bash
$ ./reset_region.py
```
```
+-----------------------------------+
|       Delete all non default      |
|    resources and sub-resources    |
+-----------------------------------+
```

#### Examples

Show some help
```bash
$ ./reset_region.py -h
```

Run on Dry Run
```bash
$ ./reset_region.py --check
```

Run on a specific region (parameter override profile)
```bash
$ ./reset_region.py --region_name=eu-central-1
```


### List Resource Groups resources

#### Description
Name: `list_resource-groups.py`
Description: Browse Resource Groups and show resources linked.
Parameters:
* `--check` : (none) Enable check mode and do not apply any action [implemented but not used yet]
* `--region_name <region>` : (string) Name of the (only one) AWS Region (e.g. eu-west-1, eu-central-1)

#### Usage
```bash
$ ./list_resource-groups.py
```
```
+----------------------------+
|    List Resource Groups    |
|         resources          |
+----------------------------+
```

#### Examples

Show some help
```bash
$ ./list_resource-groups.py -h
```

Run on Dry Run
```bash
$ ./list_resource-groups.py --check
```

Run on a specific region (parameter override profile)
```bash
$ ./list_resource-groups.py --region_name=eu-central-1
```


### List Resource Groups resources

#### Description
Name: `control_resource-groups_instances.py`
Description: Browse Resource Groups and show resources linked.
Parameters:
* `--check` : (none) Enable check mode and do not apply any action [implemented but not used yet]
* `--region_name <Region>` : (string) Name of the (only one) AWS Region (e.g. eu-west-1, eu-central-1)
* `--group_name <Resource Group>` : (string) Name of the Resource Group to control
* `--start` : (none) Start Resource Groups instances
* `--stop` : (none) Stop Resource Groups instances

#### Usage
```bash
$ ./control_resource-groups_instances.py
```
```
+----------------------------+
|    List Resource Groups    |
|         resources          |
+----------------------------+
```

#### Examples

Show some help
```bash
$ ./control_resource-groups_instances.py -h
```

Run on Dry Run
```bash
$ ./control_resource-groups_instances.py --check
```

Run on a specific region (parameter override profile)
```bash
$ ./control_resource-groups_instances.py --region_name=eu-central-1
```

Start all instances from all Resource Groups from the Region (region set in profile)
```bash
$ ./control_resource-groups_instances.py --start
```

Stop all instances included in Resource Group named `myRessGroup`
```bash
$ ./control_resource-groups_instances.py --group_name=myRessGroup --stop
```
