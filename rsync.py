import argparse
import subprocess
from loggers import logger

localdir = "/data/docs"
bucket_name = "my-bucket-name-migration"
gsutil_bin_path = "/usr/bin/gsutil"

folders = { 
  "parent" : [
    "folder1", 
    "folder2", 
    "folder3/folder31", 
    "folder4/folder41/2020", 
    "folder4/folder41/2019"
  ]
}

def run_cmd(bashCommand, print_output=False):
  logger.debug("cmd: %s" % bashCommand)
  process = subprocess.Popen(bashCommand, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  output, error = process.communicate()
  logger.debug("stdout %s" % output)
  logger.debug("stderr %s" % error)
  return (output, error, process.returncode)


def rsync_local_to_gcs():
  for category, items in folders.items(): 
    for item in items: 
      cmd = ("{gsutil_bin_path}/gsutil -m rsync -r {localdir}/{item} gs://{bucket_name}/{category}/{item}".format(
        gsutil_bin_path = gsutil_bin_path,
        localdir = localdir,
        category = category,
        item = item ,
        bucket_name = bucket_name
      ))
      run_cmd(cmd, print_output=True)

def rsync_gcs_to_local():
  for category, items in folders.items(): 
    for item in items: 
      cmd = ("mkdir -p {localdir}/{item} && {gsutil_bin_path}/gsutil -m rsync -r gs://{bucket_name}/{category}/{item} {localdir}/{item}".format(
        gsutil_bin_path = gsutil_bin_path,
        localdir = localdir,
        category = category,
        item = item ,
        bucket_name = bucket_name
      ))
      run_cmd(cmd, print_output=True)


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='GCP media synchronizer')
  parser.add_argument('--destination', help='Mode of synchronization', choices=['gcs', 'local'], required=True)
  args = parser.parse_args()
  if args.destination == 'gcs':
    rsync_local_to_gcs()
  elif args.destination == 'local' : 
    rsync_gcs_to_local()
