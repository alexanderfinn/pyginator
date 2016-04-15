import argparse
import os
import sys
import json

from configuration import Configuration
from builder import Builder
from deployer import Deployer


def main(sysargs):
    parser = argparse.ArgumentParser(description='pyginate - static web site generator')
    parser.add_argument('action', help='Action to perform', choices=['build', 'deploy'])
    parser.add_argument('-d', '--dir', help='Web site base directory', default=os.getcwd())
    parser.add_argument('-c', '--config_file_name', help='Configuration file name', default='pyginator.json')
    args = parser.parse_args()
    conf_file = os.path.join(args.dir, args.config_file_name)
    configuration = Configuration(args.dir, json.load(open(conf_file)))
    if args.action == 'build':
        builder = Builder(configuration)
        builder.build()
    elif args.action == 'deploy':
        deployer = Deployer(configuration)
        deployer.deploy()


if __name__ == '__main__':
    main(sys.argv[1:])