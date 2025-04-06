import os

import awswrangler as wr
import boto3
import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

# API endpoint to fetch random users
url = 'https://randomuser.me/api/?results=500'
# Parse API response as JSON
response3 = requests.get(url)

if response3.status_code == 200:
    Total_response = response3.json()
    final = Total_response['results']
else:
    print(f"Error: Received status code {response3.status_code}")

df = pd.json_normalize(final)

updated_df = df[[
                'gender', 'email', 'phone', 'cell', 'nat',
                'name.title', 'name.first', 'name.last',
                'location.street.number', 'location.street.name',
                'dob.date', 'registered.age'
                ]]

# AWS credentials
aws_access_key_id = os.getenv('ACCESS_KEY')
aws_secret_access_key = os.getenv('SECRET_KEY')
aws_region = os.getenv('REGION')

# session credentials
session = boto3.Session(
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=aws_region)
# the S3 path where the Parquet file will be saved
path_s3 = 's3://michael-ojo-s3-project/random_peoples_profile'

# Upload the DataFrame to S3 as a Parquet file using awswrangler
wr.s3.to_parquet(
    df=updated_df,
    path=path_s3,
    dataset=True,
    mode='append',
    boto3_session=session
    )
print(f"Data successfully uploaded to {path_s3}")
