#!/usr/bin/env bash
tmp_dir=$(mktemp -d)
echo "$tmp_dir"

# Copy local folder to temp dir
cp -r output/publish_to_kafka/local "$tmp_dir"
ls -la "$tmp_dir"

ucc-gen build

# Restore local folder
cp -r "$tmp_dir"/local output/publish_to_kafka/local