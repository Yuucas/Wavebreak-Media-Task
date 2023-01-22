import glob
from pathlib import Path
import os
from PIL import Image
import boto3

# Initiliaze the client
s3 = boto3.client('s3')

s3 = boto3.resource(
    service_name='s3',
    region_name='us-east-2',
    aws_access_key_id='AKIAUAQVCVARLH7FDWXI',
    aws_secret_access_key='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'
)

# Print out bucket names
bucket_names = []
for bucket in s3.buckets.all():
    print(bucket)
    bucket_names.append(bucket.name)
    
print(bucket_names)

# Find all image files in a directory
types = [".jpg", ".png", ".jpeg", ".avif", ".bmp", ".tiff"]
folder = Path("C:/Users/yukse/Desktop/Lectures/VSCode/Computer Vision/images_task2/")
image_files = sorted([path.as_posix() for path in filter(lambda path: path.suffix in types, folder.glob('*'))])

# Upload the images to the bucket
for image_file in image_files:
    # Get the file names
    file_path = image_file
    file_name = os.path.basename(file_path)
    print(file_name)
    
    # Upload files to S3 bucket
    s3.Bucket(bucket_names[0]).upload_file(Filename=image_file, Key=file_name)
    
# List all the image files in a given S3 bucket   
for obj in s3.Bucket(bucket_names[0]).objects.all():
    key = obj.key
    f_name = obj.bucket_name
    dict_source = {
        'Bucket' : f_name,
        'Key' : key
    }
    # Download file and read from disc
    s3.Bucket(bucket_names[0]).download_file(Key=key, Filename=f_name)
    with Image.open(f_name) as im:
        img = im
        # Check if the image has an alpha channel (transparency)
        if img.mode == "RGBA":
            # Get the image's alpha channel as a separate image
            alpha = img.split()[-1]

            # Create a new image filled with white
            white_background = Image.new("RGB", img.size, (255, 255, 255))

            # Paste the image onto the white background
            white_background.paste(img, mask=alpha)

            # Check if there are any non-white pixels in the pasted image
            if (white_background.getdata() != 255):
                    print("Image has a transparent background.")
        else:
            print("Image does not have a transparent background.")
            # Move the image to the destination bucket then delete from current bucket
            bucket_up = s3.Bucket(bucket_names[1])
            bucket_up.copy(dict_source, key)
            s3.Object(f_name, key).delete()