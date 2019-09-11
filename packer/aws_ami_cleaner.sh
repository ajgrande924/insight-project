#!/bin/bash

# bail out if anything fails
set -e

display_help () {
  echo
  echo "Usage: $0 [options]"
  echo
  echo "Options:"
  echo
  echo "  -a, --aws_account_id <id>  aws account id"
  echo "  -l, --list                 list user amis"
  echo "  -d, --delete_all           delete all user amis"
  echo "  -h, --help                 output usage information"
  echo
}

list_user_amis () {
  aws ec2 describe-images --owners ${AWS_ACCT_ID} --query 'Images[].{Name:Name,ImageId:ImageId}'
}

delete_all_user_amis () {
  # deregister images
  images_to_deregister=$(aws ec2 describe-images --owners ${AWS_ACCT_ID} --query 'Images[].{ImageId:ImageId}')
  for image_str in $images_to_deregister; do
    if [[ $image_str == *"ami-"* ]]; then
      image=$(echo $image_str | sed 's/"//g')
      echo "deregistering image: $image"
      aws ec2 deregister-image --image-id $image
    fi
  done
  
  # delete snapshots
  snapshots_to_delete=$(aws ec2 describe-snapshots --owner-ids ${AWS_ACCT_ID} --query 'Snapshots[].SnapshotId')
  for snap_str in $snapshots_to_delete; do
    if [[ $snap_str == *"snap-"* ]]; then
      snap=$(echo $snap_str | sed 's/"//g' | sed 's/,//g')
      echo "deleting snapshot: $snap"
      aws ec2 delete-snapshot --snapshot-id $snap
    fi
  done
}

while (( "$#" )); do
  case "$1" in
    -h|--help)
      display_help
      exit
      ;;
    -a|--aws_account_id)
      AWS_ACCT_ID=$2
      shift 2
      ;;
    -l|--list)
      LIST_USER_AMIS=true
      shift 1
      ;;
    -d|--delete_all)
      DELETE_ALL_USER_AMIS=true
      shift 1
      ;;
    --) # end argument parsing
      shift
      break
      ;;
    -*|--*=) # unsupported flags
      echo "Error: Unsupported flag $1" >&2
      exit 1
      ;;
    *) # preserve positional arguments
      PARAMS="$PARAMS $1"
      shift
      ;;
  esac
done

if [ -z "${AWS_ACCT_ID}" ]; then
  echo "Error: must pass an aws account id"
  exit
fi

if [ ! -z "${LIST_USER_AMIS}" ]; then
  list_user_amis
  exit
fi

if [ ! -z "${DELETE_ALL_USER_AMIS}" ]; then
  delete_all_user_amis
  exit
fi
