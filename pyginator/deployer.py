import os
import mimetypes
import boto3


class Deployer(object):

    """
    Requires ~/.aws/credentials file with the following content:
    [default]
    aws_access_key_id = YOUR_ACCESS_KEY
    aws_secret_access_key = YOUR_SECRET_KEY

    In  order to set up region creat ~/.aws/config:
    [default]
    region=us-east-1
    """
    def __init__(self, configuration):
        self.configuration = configuration

    def deploy(self):
        if not self.configuration.s3bucket:
            print "No S3 bucket specified in the configuration! Exiting."
            return
        print "Deploying to " + self.configuration.s3bucket + "..."
        s3 = boto3.resource('s3')
        for root, dirs, files in os.walk(self.configuration.target_path):
            for f in files:
                if root == self.configuration.target_path:
                    name = f
                else:
                    name = root[len(self.configuration.target_path)+1:] + '/' + f
                print "Deploying object: " + name
                data = open(os.path.join(root, f), 'rb')
                s3.Bucket(self.configuration.s3bucket).put_object(Key=name, Body=data, ContentType=mimetypes.guess_type(f)[0])
                data.close()