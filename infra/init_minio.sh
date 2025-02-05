#!/bin/sh

FLAG_FILE="/data/.initialized"

if [ ! -f "$FLAG_FILE" ]; then

  minio server /data --console-address ":9001" &
  SERVER_PID=$!

  sleep 5

  mc alias set myminio http://127.0.0.1:9000 $MINIO_ROOT_USER $MINIO_ROOT_PASSWORD
  mc mb myminio/$S3_STORAGE_BUCKET_NAME || true
  mc anonymous set public myminio/$S3_STORAGE_BUCKET_NAME

  mc admin user add myminio $S3_ACCESS_KEY_ID $S3_SECRET_ACCESS_KEY
  mc admin policy create myminio readwritelist read-write-list-policy.json
  mc admin policy attach myminio readwritelist --user $S3_ACCESS_KEY_ID



  touch "$FLAG_FILE"
  echo "------------------------- Bucket initialization is complete. -------------------------"

  kill -TERM $SERVER_PID
  wait $SERVER_PID

fi

exec minio server /data --console-address ":9001"
