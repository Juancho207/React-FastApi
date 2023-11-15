import os
import uuid
from core.config import config
import boto3


class Files:
    @staticmethod
    def upload_file(folder, file):
        file_name = f"{uuid.uuid4()}{file.filename}"
        if config.S3_ENABLED:
            s3 = Files.initialize_s3_bucket()
            file_key = (folder + '/' + file_name).replace("media/", "")

            content_type = Files.get_content_type(file.filename)
            extra_args = {"ContentType": content_type}

            s3.upload_fileobj(file.file, config.AWS_BUCKET_NAME, file_key, ExtraArgs=extra_args)
            file_url = f"{config.AWS_S3_BASE_URL}/{file_key}"
        else:
            if not os.path.exists(folder):
                os.makedirs(folder)
            file_path = os.path.join(folder, file_name)
            with open(file_path, "wb") as f:
                f.write(file.file.read())
            file_url = file_path
        return file_url

    @staticmethod
    def delete_file(folder, filename):
        if config.S3_ENABLED:
            s3 = Files.initialize_s3_bucket()
            key = filename.split(f"{config.AWS_S3_BASE_URL}/")[1]
            s3.delete_object(Bucket=config.AWS_BUCKET_NAME, Key=key)
        else:
            file_path = os.path.join(folder, filename)
            os.remove(file_path)


    @staticmethod
    def initialize_s3_bucket():
        s3 = boto3.client("s3",
                          aws_access_key_id=config.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY)
        return s3

    @staticmethod
    def get_content_type(filename):
        # Mapeo de extensiones de archivo a Content-Type
        content_type_mapping = {
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".gif": "image/gif"
        }

        # Obtén la extensión del archivo
        file_extension = os.path.splitext(filename)[1]

        # Busca el Content-Type correspondiente en el mapeo
        content_type = content_type_mapping.get(file_extension, "binary/octet-stream")
        
        return content_type
    