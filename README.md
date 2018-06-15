# AWS SDK Python scripts

Some useful scripts to list or clean entire environments.

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

## AWS onfiguration

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

#### Manual configuratoin
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
Parameters:
* `--region_name <region>` : (string) Name of the (only one) AWS Region (e.g. eu-west-1, eu-central-1)
* `--check` : (none) Enable check mode and do not apply deletions

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

