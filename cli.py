# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import argparse
import getpass
from functools import reduce


def secondsToStr(t):

    return "%d:%02d:%02d.%03d" % reduce(lambda ll, b: divmod(ll[0], b) + ll[1:], [(t * 1000,), 1000, 60, 60])


class CLI(object):

    def __init__(
        self,
        server='http://localhost:8069',
        super_user_pw='super_user_pw',
        admin_user_pw='admin_user_pw',
        data_admin_user_pw='data_admin_user_pw',
        username='username',
        password='password',
        dbname='odoo',
        db_server='localhost',
        db_user='odoo',
        db_password='odoo',
        demo_data=False,
        upgrade_all=False,
        modules_to_upgrade=[],
        lang='pt_BR',
        tz='America/Sao_Paulo'

    ):

        self.server = server  # self.server = '*'
        self.super_user_pw = super_user_pw  # self.super_user_pw = '*'
        self.admin_user_pw = admin_user_pw  # self.super_user_pw = '*'
        self.data_admin_user_pw = data_admin_user_pw  # self.data_admin_user_pw = '*'
        self.username = username  # self.username = '*'
        self.password = password  # self.password = '*'
        self.dbname = dbname  # self.dbname = '*'
        self.db_server = db_server  # self.db_server = '*'
        self.db_user = db_user  # self.db_user = '*'
        self.db_password = db_password  # self.db_password = '*'
        self.demo_data = demo_data
        self.upgrade_all = upgrade_all
        self.modules_to_upgrade = modules_to_upgrade
        self.lang = lang
        self.tz = tz

    def argparse_db_setup(self):

        parser = argparse.ArgumentParser()
        parser.add_argument('--server', action="store", dest="server")
        parser.add_argument('--super_user_pw', action="store", dest="super_user_pw")
        parser.add_argument('--admin_user_pw', action="store", dest="admin_user_pw")
        parser.add_argument('--data_admin_user_pw', action="store", dest="data_admin_user_pw")
        parser.add_argument('--db', action="store", dest="dbname")
        parser.add_argument('-d', '--demo_data', action='store_true', help='Install demo data')
        parser.add_argument('-a', '--upgrade_all', action='store_true', help='Upgrade all the modules')
        parser.add_argument('-m', '--modules', nargs='+', help='Modules to upgrade', required=False)
        parser.add_argument('--lang', action="store", dest="lang")
        parser.add_argument('--tz', action="store", dest="tz")

        args = parser.parse_args()
        # print('%s%s' % ('--> ', args))

        if args.server is not None:
            self.server = args.server
        elif self.server == '*':
            self.server = input('server: ')

        if args.super_user_pw is not None:
            self.super_user_pw = args.super_user_pw
        elif self.super_user_pw == '*':
            self.super_user_pw = getpass.getpass('super_user_pw: ')

        if args.admin_user_pw is not None:
            self.admin_user_pw = args.admin_user_pw
        elif self.admin_user_pw == '*':
            self.admin_user_pw = getpass.getpass('admin_user_pw: ')

        if args.data_admin_user_pw is not None:
            self.data_admin_user_pw = args.data_admin_user_pw
        elif self.data_admin_user_pw == '*':
            self.data_admin_user_pw = getpass.getpass('data_admin_user_pw: ')

        if args.dbname is not None:
            self.dbname = args.dbname
        elif self.dbname == '*':
            self.dbname = input('dbname: ')

        self.demo_data = args.demo_data

        self.upgrade_all = args.upgrade_all

        if args.modules is not None:
            self.modules_to_upgrade = args.modules

        if args.lang is not None:
            self.lang = args.lang

        if args.tz is not None:
            self.tz = args.tz

    def argparse_template(self):

        parser = argparse.ArgumentParser()
        parser.add_argument('--server', action="store", dest="server")
        parser.add_argument('--super_user_pw', action="store", dest="super_user_pw")
        parser.add_argument('--admin_user_pw', action="store", dest="admin_user_pw")
        parser.add_argument('--user', action="store", dest="username")
        parser.add_argument('--pw', action="store", dest="password")
        parser.add_argument('--db', action="store", dest="dbname")
        parser.add_argument('--dbserver', action="store", dest="db_server")
        parser.add_argument('--dbu', action="store", dest="db_user")
        parser.add_argument('--dbw', action="store", dest="db_password")

        args = parser.parse_args()
        # print('%s%s' % ('--> ', args))

        if args.server is not None:
            self.server = args.server
        elif self.server == '*':
            self.server = input('server: ')

        if args.super_user_pw is not None:
            self.super_user_pw = args.super_user_pw
        elif self.super_user_pw == '*':
            self.super_user_pw = getpass.getpass('super_user_pw: ')

        if args.admin_user_pw is not None:
            self.admin_user_pw = args.admin_user_pw
        elif self.admin_user_pw == '*':
            self.admin_user_pw = getpass.getpass('admin_user_pw: ')

        if args.dbname is not None:
            self.dbname = args.dbname
        elif self.dbname == '*':
            self.dbname = input('dbname: ')

        if args.username is not None:
            self.username = args.username
        elif self.username == '*':
            self.username = input('username: ')

        if args.password is not None:
            self.password = args.password
        elif self.password == '*':
            self.password = getpass.getpass('password: ')

        if args.db_server is not None:
            self.db_server = args.db_server
        elif self.db_server == '*':
            self.db_server = input('db_server: ')

        if args.db_user is not None:
            self.db_user = args.db_user
        elif self.db_user == '*':
            self.db_user = input('db_user: ')

        if args.db_password is not None:
            self.db_password = args.db_password
        elif self.db_password == '*':
            self.db_password = getpass.getpass('db_password: ')


class CLI2(object):

    def __init__(
        self,
        local_server='http://localhost:8069',
        local_admin_user_pw='local_admin_user_pw',
        local_user='local_user',
        local_user_pw='local_user_pw',
        local_dbname='local_dbname',
        remote_server='http://remotehost:8069',
        remote_admin_user_pw='remote_admin_user_pw',
        remote_user='remote_use_rname',
        remote_user_pw='remote_user_pw',
        remote_dbname='remote_dbname',
    ):

        self.local_server = local_server  # self.local_server = '*'
        self.local_admin_user_pw = local_admin_user_pw  # self.local_admin_user_pw = '*'
        self.local_user = local_user  # self.local_user = '*'
        self.local_user_pw = local_user_pw  # self.local_user_pw = '*'
        self.local_dbname = local_dbname  # self.local_dbname = '*'
        self.remote_server = remote_server  # self.remote_server = '*'
        self.remote_admin_user_pw = remote_admin_user_pw  # self.remote_admin_user_pw = '*'
        self.remote_user = remote_user  # self.remote_user = '*'
        self.remote_user_pw = remote_user_pw  # self.remote_user_pw = '*'
        self.remote_dbname = remote_dbname  # self.remote_dbname = '*'

    def argparse(self):

        parser = argparse.ArgumentParser()
        parser.add_argument('--lserver', action="store", dest="local_server")
        parser.add_argument('--ladmin_pw', action="store", dest="local_admin_user_pw")
        parser.add_argument('--luser', action="store", dest="local_user")
        parser.add_argument('--lpw', action="store", dest="local_user_pw")
        parser.add_argument('--ldb', action="store", dest="local_dbname")
        parser.add_argument('--rserver', action="store", dest="remote_server")
        parser.add_argument('--radmin_pw', action="store", dest="remote_admin_user_pw")
        parser.add_argument('--ruser', action="store", dest="remote_user")
        parser.add_argument('--rpw', action="store", dest="remote_user_pw")
        parser.add_argument('--rdb', action="store", dest="remote_dbname")

        args = parser.parse_args()
        # print('%s%s' % ('--> ', args))

        if args.local_server is not None:
            self.local_server = args.local_server
        elif self.local_server == '*':
            self.local_server = input('local_server: ')

        if args.local_admin_user_pw is not None:
            self.local_admin_user_pw = args.local_admin_user_pw
        elif self.local_admin_user_pw == '*':
            self.local_admin_user_pw = getpass.getpass('local_admin_user_pw: ')

        if args.local_user is not None:
            self.local_user = args.local_user
        elif self.local_user == '*':
            self.local_user = getpass.getpass('local_user: ')

        if args.local_user_pw is not None:
            self.local_user_pw = args.local_user_pw
        elif self.local_user_pw == '*':
            self.local_user_pw = getpass.getpass('local_user_pw: ')

        if args.local_dbname is not None:
            self.local_dbname = args.local_dbname
        elif self.local_dbname == '*':
            self.local_dbname = input('local_dbname: ')

        if args.remote_server is not None:
            self.remote_server = args.remote_server
        elif self.remote_server == '*':
            self.remote_server = input('remote_server: ')

        if args.remote_admin_user_pw is not None:
            self.remote_admin_user_pw = args.remote_admin_user_pw
        elif self.remote_admin_user_pw == '*':
            self.remote_admin_user_pw = getpass.getpass('remote_admin_user_pw: ')

        if args.remote_user is not None:
            self.remote_user = args.remote_user
        elif self.remote_user == '*':
            self.remote_user = getpass.getpass('remote_user: ')

        if args.remote_user_pw is not None:
            self.remote_user_pw = args.remote_user_pw
        elif self.remote_user_pw == '*':
            self.remote_user_pw = getpass.getpass('remote_user_pw: ')

        if args.remote_dbname is not None:
            self.remote_dbname = args.remote_dbname
        elif self.remote_dbname == '*':
            self.remote_dbname = input('remote_dbname: ')
