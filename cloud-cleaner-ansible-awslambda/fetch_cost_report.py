import boto3

bucket = "cloud-cost-reports-analysis"  # 🔁 replace with your actual S3 bucket name
prefix = "underutilized_report_"

s3 = boto3.client("s3")

# Get the latest report
objects = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
files = sorted(objects.get("Contents", []), key=lambda x: x["LastModified"], reverse=True)

if files:
    key = files[0]["Key"]
    s3.download_file(bucket, key, "latest_report.csv")
    print(f"Downloaded: {key}")
else:
    print("No report found.")