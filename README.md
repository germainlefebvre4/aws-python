# Dependencies
You need to install python boto3 libraries before using the scripts. It will able scripts to use AWS API.
```
yum install python2-boto3
```


## Configure user session
To use AWS API calls you need to make your account reachable with Access ID.

On AWS go to : AWS/IAM/Users/[MyUser] then "Security Credentials" and "Create access key". Save Key ID and Access Key before closing.

### Option 1 : Smart configuration
Run `aws configure` and fill the fields `ACCESS_KEY`, `SECRET`and `REGION`.
```
$ aws configure
```

### Option 2 : Manuel configuratoin
On Linux session fill the configuration file at `~/.aws/credentials` :
```
$ vi ~/.aws/credentials
```
```
[default]
aws_access_key_id = ***********
aws_secret_access_key = *********************
```

```
$ vi ~/.aws/config
```
```
[default]
region = eu-central-1 # Optional
```

# Scripts

## Delete VPCs resources : delete_vpcs.py

Reset resources from an account depending on the region you mentioned (config or parameter).


### Warning

You need to provide API Key with high rights elevation on AWS.

### Usage

```
$ ./delete_vpcs.py
```

```
Region is not defnied. You can define it in :
 - Arguments
 - File ~/.aws/config ([default] section)
```

### Arguments

Script arguments :

`--region_name` : Takes the name of the AWS Region (eu-west-1, eu-central-1)

`--check` : No argument. Enable check mode and do not apply deletions

### Examples

```
$ ./delete_vpcs.py
```

```
+-----------------------------------+
|    Delete non default VPCs and    |
|       and its sub-resources       |
+-----------------------------------+
```


```
$ ./delete_vpcs.py -h
```

```
$ ./delete_vpcs.py --check
```

```
$ ./delete_vpcs.py --region_name=eu-central-1
```


## List non default VPCs and Instances with their creator : list_region_vpc.py

### Usage

```
$ ./list_region_vpc.py
```

### Arguments
`--check` : No argument. Enable check mode and do not apply deletions

### Examples

```
$ ./list_region_vpc.py
```

```
+-------------------------------------------+
|    List non default VPCs and Instances    |
|      for all regions with its owner.      |
+-------------------------------------------+
Regions: ap-northeast-1, ap-northeast-2, ap-south-1, ap-southeast-1, ap-southeast-2, ca-central-1, eu-central-1, eu-west-1, eu-west-2, sa-east-1, us-east-1, us-east-2, us-west-1, us-west-2
```


```
$ ./list_region_vpc.py -h
```

```
$ ./list_region_vpc.py --check
```

