## Install dependencies
You need to install python boto3 libraries before using the scripts. It will able scripts to use AWS API.
```
yum install python2-boto3
```


### Configure user session
To use AWS API calls you need to make your account reachable with Access ID.

On AWS go to : AWS/IAM/Users/[MyUser] then "Security Credentials" and "Create access key". Save Key ID and Access Key before closing.

On Linux session fill the configuration file at `~/.aws/credentials` :
```
vi ~/.aws/credentials
```

```
[default]
aws_access_key_id = ***********
aws_secret_access_key = *********************
#region = eu-central-1 # Optional
```

### Run scripts
Make your scripts runnable.
```
chmod u+x list_resources.py
```


Run simply the scripts.
```
./list_resources.py
```

```
Dev i-07c96af5990dc9de0 ami-e28d098d vpc-90e3caf9 germain.lefebvre
```

## Description scripts

### Reset account resources

Reset resources from an account depending on the region you mentioned (config or parameter).


#### Warning

You need to provide API Key with high rights elevation on AWS.

#### Usage

`./reset_account.py`
```
Region is not defnied. You can define it in :
 - Arguments
 - File ~/.aws/config ([default] section)
```

#### Arguments
`--region_name` : Takes the name of the AWS Region (eu-west-1, eu-central-1)

#### Examples

`./delete_vpc.py`

`./delete_vpc.py --region_name=eu-central-1`

