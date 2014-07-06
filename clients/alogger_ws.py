#! /usr/bin/env python

# Copyright 208-2014 VPAC
#
# This file is part of python-alogger.
#
# python-alogger is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# python-alogger is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with python-alogger  If not, see <http://www.gnu.org/licenses/>.

import xmlrpclib
import datetime
import sys
import os
import getopt
import ConfigParser

CONFIG_FILE = '/usr/local/etc/alogger_ws.cfg'


def parse_logs(date, cfg, debug=False):

    filename = date.strftime('%Y%m%d')

    try:
        f = open('%s/%s' % (cfg['LOG_DIR'], filename), 'r')
    except:
        if debug:
            print(
                'ERROR: failed to open file %s/%s'
                % (cfg['LOG_DIR'], filename))
        sys.exit(1)

    data = f.readlines()
    if data:

        server = xmlrpclib.Server(cfg['WS_URL'])

        try:
            summary, output = server.parse_usage(
                cfg['WS_USERNAME'], cfg['WS_PASSWORD'], data, str(date),
                cfg['MACHINE_NAME'], cfg['LOG_TYPE'])
            if debug:
                print(summary)

            for line in output:
                print line

        except:
            print(summary)
            print(output)
            raise


def print_help():
    print('Usage:')
    print('')
    print('  -h  -  Print help')
    print('  -f  -  Specify log file eg. 20071225')
    print('  -y  -  proccess yesterdays log file')
    print('  -A  -  Read all log files')
    print('  -d  -  Print Debug information')
    print('')


def write_config():
    config = ConfigParser.RawConfigParser()

    config.add_section('Default')
    print('No configuration file found.')
    machine_name = raw_input('Enter machine name: ')
    config.set('Default', 'machine_name', machine_name)
    log_dir = raw_input(
        'Log directory: [/usr/spool/PBS/server_priv/accounting] ')
    config.set(
        'Default', 'log_dir',
        log_dir or '/usr/spool/PBS/server_priv/accounting')
    log_type = raw_input('Log type: [PBS] ')
    config.set('Default', 'log_type', log_type or 'PBS')
    ws_url = raw_input('Web service url: ')
    config.set('Default', 'ws_url', ws_url)
    ws_username = raw_input('Web service username: ')
    config.set('Default', 'ws_username', ws_username)
    ws_password = raw_input('Web service password: ')
    config.set('Default', 'ws_password', ws_password)

    # Writing our configuration file to 'example.cfg'
    f = open(CONFIG_FILE, 'wb')
    config.write(f)
    f.close()


def get_config():

    if not os.path.isfile(CONFIG_FILE):
        write_config()

    config = ConfigParser.RawConfigParser()

    config.read(CONFIG_FILE)
    cfg = {}
    try:
        cfg['MACHINE_NAME'] = config.get('Default', 'machine_name')
        cfg['LOG_DIR'] = config.get('Default', 'log_dir')
        cfg['LOG_TYPE'] = config.get('Default', 'log_type')
        cfg['WS_URL'] = config.get('Default', 'ws_url')
        cfg['WS_USERNAME'] = config.get('Default', 'ws_username')
        cfg['WS_PASSWORD'] = config.get('Default', 'ws_password')
    except:
        write_config()
        get_config()

    return cfg


if __name__ == "__main__":

    debug = False
    opts, args = getopt.getopt(sys.argv[1:], 'yAhdf:')
    opts = dict(opts)

    if not opts or '-h' in opts:
        print_help()
        sys.exit(1)

    cfg = get_config()

    if '-d' in opts:
        debug = True

    if '-A' in opts:
        file_list = os.listdir(cfg['LOG_DIR'])

        for filename in file_list:
            date = datetime.date(
                int(filename[:4]), int(filename[4:6]), int(filename[6:]))
            parse_logs(date, cfg, debug)
        sys.exit(0)

    if '-f' in opts:
        filename = opts['-f']
        date = datetime.date(
            int(filename[:4]), int(filename[4:6]), int(filename[6:]))
    elif '-y' in opts:
        date = datetime.date.today() - datetime.timedelta(days=1)
    else:
        print 'ERROR: You must specify either -f or -y'

    parse_logs(date, cfg, debug)

    sys.exit(0)
