# https://dzone.com/articles/boto3-amazon-s3-as-python-object-store
# https://www.peterbe.com/plog/fastest-way-to-find-out-if-a-file-exists-in-s3
import boto3
import json
import pickle
from datetime import date
import json
import os
import logging


env=os.getenv('ENVIRONMENT','dev')
external_log_level=os.getenv('EXTERNAL_LOG_LEVEL','INFO')
internal_log_level=os.getenv('INTERNAL_LOG_LEVEL','DEBUG')
logging.basicConfig(level=external_log_level)
logging.getLogger(__name__).setLevel(internal_log_level)
logger = logging.getLogger(__name__)
s3 = boto3.client('s3')

def s3_retrieve_dict(bucketname,key):
    d_object = s3.get_object(Bucket=bucketname,Key=key)
    serializedObject = d_object['Body'].read()
    myData = json.loads(serializedObject)
    return myData

def s3_put_dict(dict_obj,bucketname,key):
    myData = dict_obj
    serializedMyData = json.dumps(myData)
    s3.put_object(Bucket=bucketname,Key=key,Body=serializedMyData)


def s3_retrieve_rows(bucketname,key):
    #Connect to S3
    #Read the object stored in key 'myList001'
    s3_object = s3.get_object(Bucket=bucketname,Key=key)
    serializedObject = s3_object['Body'].read()
    #Deserialize the retrieved object
    myList = pickle.loads(serializedObject)
    return myList

def s3_put_rows(row_list,bucketname,key):
    myList=row_list
    #Serialize the object 
    serializedListObject=pickle.dumps(myList)
    
    serializedListObject="\n".join(myList)

    
    logger.debug(myList)
    #Write to Bucket named 'mytestbucket' and 
    #Store the list using key myList001
    s3.put_object(Bucket=bucketname,Key=key,Body=serializedListObject)

def s3_exists(bucketname,key):
    """return the key's size if it exist, else None"""
    response = s3.list_objects_v2(
        Bucket=bucketname,
        Prefix=key
    )
    for obj in response.get('Contents', []):
        if obj['Key'] == key:
            return True
    return False

def main():
    today = date.today().strftime("%d.%m.%Y")
    bucketname='tartuvarjupaik'
    key='tracker'
    if not s3_exists(bucketname=bucketname,key=key):
        s3_put_rows(row_list=[{'today': today}],bucketname=bucketname,key=key)
        my_list=s3_retrieve_rows(bucketname=bucketname,key=key)
        print(my_list)
    else: 
        print("Rows do exist")
        my_list=s3_retrieve_rows(bucketname=bucketname,key=key)
        print(my_list)    

    key='dog_count'
    if not s3_exists(bucketname=bucketname,key=key):
        s3_put_dict(dict_obj={'today': today},bucketname=bucketname,key=key)
        my_list=s3_retrieve_dict(bucketname=bucketname,key=key)
        print(my_list)
    else: 
        print("Rows do exist")
        my_list=s3_retrieve_dict(bucketname=bucketname,key=key)
        print(my_list)    

    
if __name__== "__main__":
  main()