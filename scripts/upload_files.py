import boto3
import sys
import os
from scripts.pdf_to_img import to_jpg


def upload_files(input_path: str, s3bucket: str, bucket_path: str):
    """ Upload JPEG file(s) to designated S3 bucket directory.

    Args:
        input_path (str): Input directory.
        s3bucket (str): S3 bucket name.
        bucket_path (str): Directory within the bucket.

    Raises:
        ValueError: Non-existence of input path.
    """
    if not os.path.exists(input_path):  # check file existence.
        raise ValueError(f"DOES NOT EXIST: '{folder_path}'")

    s3 = boto3.resource('s3')
    bucket = s3.Bucket(s3bucket)

    for subdir, _, files in os.walk(input_path):
        for file in files:
            full_path = os.path.join(subdir, file)
            if file.lower().endswith("jpg") | file.lower().endswith("jpeg"):
                with open(full_path, 'rb') as data:
                    bucket.put_object(Key=bucket_path + '/' +
                                      full_path[len(input_path) + 1:],
                                      Body=data)
                    print(f"UPLOADED: {file}")
            else:
                print(f"FILE: '{full_path}' is not JPEG file. SKIPPED.")


if __name__ == "__main__":
    # cml inputs.
    folder_path = sys.argv[1]  # image folder path
    s3bucket = sys.argv[2]  # s3 bucket name
    bucket_dir = sys.argv[3]  # separate directory within s3 bucket

    if not os.path.exists(folder_path):
        raise ValueError(
            f"Directory: '{folder_path}' does not exist, check the path again."
        )

    print("***** Uploading images to S3 *****")
    print("--------------------------------")
    print(f"Image Folder Path: {folder_path}")
    print(f"S3 Bucket: {s3bucket}")
    print(f"S3 Directory: {bucket_dir}")
    print("-------------------------------- \n")
    upload_files(folder_path, s3bucket, bucket_dir)
