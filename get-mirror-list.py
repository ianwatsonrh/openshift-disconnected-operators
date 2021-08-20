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

def main():
  operators = mirror_operator_catalogue.GetWhiteListedOperators()
  print(str(mirror_operator_catalogue.GetListOfCommaDelimitedOperatorList(operators)))

if __name__ == "__main__":
  main()
