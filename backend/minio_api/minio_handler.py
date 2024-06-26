import os
from typing import BinaryIO

import jwt
import minio
from jwt.exceptions import DecodeError
from starlette.responses import JSONResponse


class MinioHandler:
    def __init__(
        self,
        minio_endpoint: str,
        api_endpoint: str,
        access_key: str,
        secret_key: str,
        bucket: str,
        secure: bool = False,
    ):
        self.client = minio.Minio(
            minio_endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=secure,
        )
        self.bucket = bucket
        self.endpoint_api = api_endpoint
        self.secure = secure

    def decode_token(self, token: str):
        try:
            return jwt.decode(
                token,
                os.getenv('JWT_SECRET'),
                algorithms=["HS256"],
            )
        except DecodeError:
            return JSONResponse(
                {
                    "status": "failed",
                    "reason": "Link expired or invalid",
                },
                status_code=400,
            )

    def put_file(self, name: str, file: BinaryIO, length: int):
        self.client.put_object(self.bucket, name, file, length=length)
        obj = self.stats(name)
        payload = {
            "filename": obj.object_name,
        }
        encoded_jwt = jwt.encode(
            payload,
            os.getenv('JWT_SECRET'),
            algorithm="HS256",
        )
        link = (
            f'{"https://" if self.secure else "http://"}'
            f'{self.endpoint_api}/memes/download/'
            f'{encoded_jwt}/'
        )
        return link

    def remove_file(self, old_name: str):
        temp_link = old_name.rsplit("/", 2)[-2]
        decoded_jwt = self.decode_token(temp_link)
        filename = decoded_jwt['filename']
        self.client.remove_object(self.bucket, filename)

    def stats(self, name: str) -> minio.api.Object:
        return self.client.stat_object(self.bucket, name)

    def download_file(self, name: str):
        info = self.client.stat_object(self.bucket, name)
        total_size = info.size
        offset = 0
        while True:
            response = self.client.get_object(
                self.bucket,
                name,
                offset=offset,
                length=2048,
            )
            yield response.read()
            offset = offset + 2048
            if offset >= total_size:
                break
