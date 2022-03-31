from time import sleep
import boto3 
import os 
import logging

#Get Env Variables
patch_group   = os.environ['patch_group']  

#Set Logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

#Set boto3 clients
ec2 = boto3.resource('ec2')

def lambda_handler(event, context):
    filters = [{
            'Name': 'tag:Patch Group',
            'Values': [patch_group]  
        },
        {
            'Name': 'instance-state-name', 
            'Values': ['stopped']
        }
    ]    
    instances = ec2.instances.filter(Filters=filters)    # Use the filter() method of the instances collection to retrieve all stopped EC2 instances with the specific tag.
    stoppedInstances = [instance.id for instance in instances]
    if len(stoppedInstances) > 0:
        startingUp = ec2.instances.filter(InstanceIds=stoppedInstances).start()        #perform the startup 

        for instance in stoppedInstances:
            ec2.create_tags(Resources=[instance], Tags=[{'Key': 'Status Instance', 'Value':'stopped'}])
    sleep(200)
