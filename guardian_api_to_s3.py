import os

import awswrangler as wr
import boto3
import pandas as pd
import requests
from dotenv import load_dotenv
from ENDPOINT import endpoint

load_dotenv()


def call_guardian_api():
    # Sending a GET request to the endpoint
    response = requests.get(endpoint)
    if response.status_code == 200:
        Data = response.json()

        checkout = Data['response']['results']
        Nigeria_guardian_api = []
        for Nigeria in checkout:
            Nigeria_guardian_api.append({
                'type': Nigeria['type'],
                'sectionId': Nigeria['sectionId'],
                'webPublicationDate': Nigeria['webPublicationDate'],
                'webTitle': Nigeria['webTitle']
             })
        return Nigeria_guardian_api


# create a dataframe from the call_guardian_api function
df = pd.DataFrame(call_guardian_api())
dataframe = pd.DataFrame(call_guardian_api())

# AWS credentials
aws_access_key_id = os.getenv('ACCESS_KEY')
aws_secret_access_key = os.getenv('SECRET_KEY')
aws_region = os.getenv('REGION')


# session credentials
session = boto3.Session(
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=aws_region
)

# the S3 path where the Parquet file will be saved
path_s3 = 's3://michael-ojo-s3-project/nigeria_guardian_api'

# Upload the DataFrame to S3 as a Parquet file using awswrangler
wr.s3.to_parquet(
    df=dataframe,
    path=path_s3,
    dataset=True,
    mode='append',
    boto3_session=session)

print(f"Data successfully uploaded to {path_s3}")
