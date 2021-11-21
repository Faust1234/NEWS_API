import csv
import datetime
import boto3

from app.core.config import settings

ct = datetime.datetime.now().timestamp()


def create_csv_file(data_file):
    with open(f'{ct}-example4.csv', 'w') as csv_file:
        fieldnames = ['Title', 'Source', 'Url']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for i in data_file:
            writer.writerow({'Title': i[0], 'Source': i[1], 'Url': i[2]})
        return csv_file.name


def s3_endpoint(file_name):
    session = boto3.Session(
        aws_access_key_id=settings.S3_ACCESS_KEY,
        aws_secret_access_key=settings.S3_SECRET_KEY
    )
    s3 = session.resource('s3')
    s3_object = s3.Object(settings.S3_BUCKET_NAME, file_name)

    result = s3_object.put(Body=open(f'{file_name}', 'rb'))

    res = result.get('ResponseMetadata')

    if res.get('HTTPStatusCode') == 200:
        return 'File Uploaded Successfully'
    else:
        return 'File Not Uploaded'
