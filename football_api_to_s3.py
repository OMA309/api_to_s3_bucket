import os

import awswrangler as wr
import boto3
import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

# API endpoint to fetch football competitions
url = 'http://api.football-data.org/v4/competitions/'


# Send request to the API
football = requests.get(url)

if football.status_code == 200:
    compete = football.json()
    Result = compete['competitions']
    df = pd.json_normalize(Result)
else:
    print(f"Error: Received status code {football.status_code}")

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
path_s3 = 's3://michael-ojo-s3-project/football_competition'

# Upload the DataFrame to S3 as a Parquet file using awswrangler
wr.s3.to_parquet(
    df=df,
    path=path_s3,
    dataset=True,
    mode='append',
    boto3_session=session)

# Print a success message after the upload is complete
print(f"Data successfully uploaded to {path_s3}")
