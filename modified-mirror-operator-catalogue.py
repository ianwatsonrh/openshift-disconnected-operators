#!/usr/bin/env python3
import os
import sys
import re
import tarfile
import yaml
import subprocess
import argparse
import urllib.request
from jinja2 import Template
from pathlib import Path
import upgradepath
import sqlite3
import mirror_operator_catalogue

def is_number(string):
  try:
      float(string)
      return True
  except ValueError:
      return False

def main():

  script_root_dir = "/var/lib/registry"
  run_root_dir = os.path.join(script_root_dir, "run")
  publish_root_dir = os.path.join(script_root_dir, "output")
  mirror_summary_file = os.path.join(publish_root_dir, 'mirror_log.txt')
  operator_output_file = os.path.join(publish_root_dir, 'offline_operators.yaml') 

  run_temp = os.path.join(run_root_dir, "temp")
  mirror_summary_path = Path(mirror_summary_file)
  operator_output_path = Path(operator_output_file)

  # Create publish, run and temp paths
  mirror_operator_catalogue.RecreatePath(publish_root_dir)
  mirror_operator_catalogue.RecreatePath(run_root_dir)
  mirror_operator_catalogue.RecreatePath(run_temp)

  print("Getting the list of operators for custom catalogue..")
  operators = mirror_operator_catalogue.GetWhiteListedOperators()

  print("Extracting custom catalogue database...")
  db_path = mirror_operator_catalogue.ExtractIndexDb()
  
  print("Create upgrade matrix for selected operators...")
  for operator in operators:
    operator.upgrade_path, operator.latest_version = upgradepath.GetShortestUpgradePath(operator.name, operator.start_version, db_path)  

  print("Getting list of images to be mirrored...")
  mirror_operator_catalogue.GetImageListToMirror(operators, db_path)

  print("Writing summary data..")
  mirror_operator_catalogue.CreateSummaryFile(operators, mirror_summary_path)

  mirror_operator_catalogue.CreateOutputOperatorsFile(operators, operator_output_path)

  images = mirror_operator_catalogue.getImages(operators)

  print("Creating Image Content Source Policy YAML...")
  mirror_operator_catalogue.CreateImageContentSourcePolicyFile(images)

  print("Creating Mapping File...")
  mirror_operator_catalogue.CreateMappingFile(images)

  print("Creating Image manifest file...")
  mirror_operator_catalogue.CreateManifestFile(images)
  print("Creating Catalog Source YAML...")
  mirror_operator_catalogue.CreateCatalogSourceYaml(mirror_operator_catalogue.custom_redhat_operators_catalog_image_url)

  print("Catalogue creation and image mirroring complete")
  print("See Publish folder for the image content source policy and catalog source yaml files to apply to your cluster")

  cmd_args = "rm -rf {}".format(run_root_dir)
  subprocess.run(cmd_args, shell=True, check=True)


if __name__ == "__main__":
  main()
