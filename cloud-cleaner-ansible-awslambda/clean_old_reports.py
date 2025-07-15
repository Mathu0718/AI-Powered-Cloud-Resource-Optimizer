# clean_old_reports.py
import boto3

bucket = "cloud-cost-reports-analysis"  # replace with your bucket
prefix = "underutilized_report_"

s3 = boto3.client("s3")
objects = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)

files = sorted(objects.get("Contents", []), key=lambda x: x["LastModified"])

if len(files) > 10:
    delete_count = len(files) - 10
    for file in files[:delete_count]:
        print(f"🗑️ Deleting {file['Key']}")
        s3.delete_object(Bucket=bucket, Key=file["Key"])
    print(f"✅ Deleted {delete_count} old reports.")
else:
    print("✅ No old reports to delete.")
