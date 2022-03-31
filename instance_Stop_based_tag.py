from time import sleep
import boto3 
import os 
import logging

#Set Logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

#Set boto3 clients
ec2 = boto3.resource('ec2')
client = boto3.client('ec2')

def lambda_handler(event, context):
    sleep(300)
    filters = [{
            'Name': 'tag:Status Instance',
            'Values': ['stopped']
        },
        {
            'Name': 'instance-state-name', 
            'Values': ['running']
        }
    ]    
    
    instances = ec2.instances.filter(Filters=filters)    # Use the filter() method of the instances collection to retrieve all Running EC2 instances with the specific tag.
    RunningInstances = [instance.id for instance in instances]
    if len(RunningInstances) > 0:
        shuttingDown = ec2.instances.filter(InstanceIds=RunningInstances).stop()    #  perform Shutting Down

        for instance in RunningInstances :
            client.delete_tags(Resources=[instance], Tags=[{'Key': 'Status Instance', 'Value':'stopped'}])


