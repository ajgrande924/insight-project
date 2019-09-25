import boto3

s3 = boto3.resource('s3')
for bucket in s3.buckets.all():
    print(bucket.name)


# Set s3-boto config
s3_bucket = 'lmd-midi'
s3 = boto3.resource('s3')
boto_client = boto3.client('s3')
bucket = s3.Bucket(s3_bucket)

for obj in bucket.objects.all():
    print(obj.key)