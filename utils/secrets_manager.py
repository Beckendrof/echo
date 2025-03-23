try:
    import os
    import json
    import boto3
    from botocore.exceptions import ClientError

except Exception as e:
    raise (f"Some modules are missing : {e}")


def get_secret(secret_name, region_name):
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except client.exceptions.ResourceNotFoundException:
        print(f"The requested secret {secret_name} was not found")
        return None
    except client.exceptions.InvalidRequestException as e:
        print(f"The request was invalid: {e}")
        return None
    except client.exceptions.InvalidParameterException as e:
        print(f"The request had invalid parameters: {e}")
        return None
    else:
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
            return json.loads(secret)
        else:
            decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])
            return json.loads(decoded_binary_secret)




