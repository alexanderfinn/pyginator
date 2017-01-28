import argparse
import os
import sys
import json

from configuration import Configuration
from builder import Builder
from deployer import Deployer
from processor import Processor


def main():
    parser = argparse.ArgumentParser(description='pyginate - static web site generator')
    parser.add_argument('action', help='Action to perform', choices=['build', 'deploy', 'process'])
    parser.add_argument('-d', '--dir', help='Web site base directory', default=os.getcwd())
    parser.add_argument('-c', '--config_file_name', help='Configuration file name', default='pyginator.json')
    parser.add_argument('-s', '--processing_script', help='Procesing script to apply', default='')
    parser.add_argument('-dr', '--dry_run', action='store_true', help='Do not apply any changes, just report')
    args = parser.parse_args()
    conf_file = os.path.join(args.dir, args.config_file_name)
    configuration = Configuration(args.dir, json.load(open(conf_file)))
    if args.action == 'build':
        builder = Builder(configuration)
        builder.build()
    elif args.action == 'deploy':
        deployer = Deployer(configuration)
        deployer.deploy()
    elif args.action == 'process':
        if args.dry_run:
            configuration.dry_run = True
        processor = Processor(configuration, args.processing_script)
        processor.process()


if __name__ == '__main__':
    main()