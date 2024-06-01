import os

from minio import Minio
from minio.error import S3Error

import logging
logger = logging.getLogger(__name__)


class MinioConfig:
    def __init__(self):
        self.MINIO_ENDPOINT = os.getenv('MINIO_ENDPOINT', 'minioserver:9000')
        self.MINIO_BUCKET = os.getenv('MINIO_BUCKET', 'mediae')
        self.AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
        self.AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
        self.minio_client = self.initialize_minio_client()
           
    def initialize_minio_client(self):
        return Minio (
            self.MINIO_ENDPOINT,
            access_key=self.AWS_ACCESS_KEY_ID,
            secret_key=self.AWS_SECRET_ACCESS_KEY,
            secure=False
        )
        
    def __repr__(self):
        return f"MinioConfig(MINIO_ENDPOINT='{self.MINIO_ENDPOINT}', MINIO_BUCKET='{self.MINIO_BUCKET}', AWS_ACCESS_KEY_ID='{self.AWS_ACCESS_KEY_ID}', AWS_SECRET_ACCESS_KEY='*****')"





def ensure_minio_bucket_exists(minio_config: MinioConfig):
    logger.info("Ensuring MinIO bucket exists...")
    try:
        if not minio_config.minio_client.bucket_exists(minio_config.MINIO_BUCKET):
            logger.info("Bucket does not exist. Creating bucket: %s", minio_config.MINIO_BUCKET)
            minio_config.minio_client.make_bucket(minio_config.MINIO_BUCKET)
        else:
            logger.info("Bucket already exists: %s", minio_config.MINIO_BUCKET)
    except S3Error as e:
        logger.error("Failed to ensure MinIO bucket: %s", e)
        raise