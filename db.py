# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

import erppeek  # http://erppeek.readthedocs.io/en/1.6.2/api.html#manage-addons
import xmlrpc.client as xmlrpclib

logging.basicConfig(level=logging.DEBUG)
_logger = logging.getLogger(__name__)


class DB(object):

    def __init__(
        self,
        server='http://localhost:8069',
        super_user_pw='super_user_pw',
        admin_user_pw='admin_user_pw',
        data_admin_user_pw='data_admin_user_pw',
        dbname='odoo',
        demo_data=False,
        upgrade_all=False,
        modules_to_upgrade=[],
        lang='pt_BR',
        tz='America/Sao_Paulo'
    ):

        self.server = server
        self.super_user_pw = super_user_pw
        self.admin_user_pw = admin_user_pw
        self.data_admin_user_pw = data_admin_user_pw
        self.dbname = dbname
        self.demo_data = demo_data
        self.upgrade_all = upgrade_all
        self.modules_to_upgrade = modules_to_upgrade
        self.lang = lang
        self.tz = tz

    def create(self):

        url = self.server
        sock_common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
        _logger.info(u'--> sock_common.version(): "{0}"'.format(sock_common.version()))

        client = erppeek.Client(server=self.server)
        _logger.info(u'--> Databases found: "{0}"'.format(client.db.list()))

        if self.dbname not in client.db.list():

            _logger.info(u'--> Creating database "{0}"...'.format(self.dbname))

            client.create_database(
                passwd=self.super_user_pw,
                database=self.dbname,
                demo=self.demo_data,
                lang=self.lang,
                user_password=self.admin_user_pw
            )

            _logger.info(u'--> Done.')
            return True

        else:

            _logger.info(u'--> Database "{0}" already exists.'.format(self.dbname))
            _logger.info(u'--> Done.')
            return False

    def my_company_setup(self, CompanyName, website, Company_image):

        print('Configuring My Company...')

        client = erppeek.Client(
            server=self.server,
            db=self.dbname,
            user='admin',
            password=self.admin_user_pw)

        ResPartner = client.model('res.partner')
        args = [('name', '=', 'My Company'), ]
        partner_id = ResPartner.browse(args).id

        if partner_id != []:

            values = {
                'name': CompanyName,
                'email': '',
                'website': website,
                'tz': self.tz,
                'lang': self.lang,
                'image_1920': Company_image,
            }
            ResPartner.write(partner_id, values)

            ResCompany = client.model('res.company')
            args = [('name', '=', 'My Company'), ]
            company_id = ResCompany.browse(args).id

            values = {
                'name': CompanyName,
                'email': '',
                'website': website,
                'logo': Company_image,
            }
            ResCompany.write(company_id, values)

            print('Done.')

        else:

            # print('"{0}" already configured.'.format(self.dbname))
            print('"{0}" already configured.'.format(CompanyName))
            # print('Done.')

    # def administrator_setup(self, admin_user_email, Administrator_image):

    #     print('Configuring user "Administrator"...')

    #     client = erppeek.Client(
    #         server=self.server,
    #         db=self.dbname,
    #         user='admin',
    #         password=self.admin_user_pw)

    #     ResUsers = client.model('res.users')
    #     args = [('name', '=', 'Administrator'), ]
    #     user = ResUsers.browse(args)

    #     if user[0].email != admin_user_email:

    #         values = {
    #             'lang': self.lang,
    #             'tz': self.tz,
    #             'email': admin_user_email,
    #             'image_1920': Administrator_image,
    #         }
    #         ResUsers.write(user.id, values)

    #         group_name_list = [
    #             'Contact Creation',
    #         ]
    #         self.user_groups_setup('Administrator', group_name_list)

    #         print('Done.')

    #     else:

    #         print('User "{0}" already configured.'.format(user.name))
    #         print('Done.')

    def administrator_setup(self, admin_user_email, Administrator_image):

        print('Configuring user "Administrator"...')

        client = erppeek.Client(
            server=self.server,
            db=self.dbname,
            user='admin',
            password=self.admin_user_pw)

        ResUsers = client.model('res.users')
        args = [('name', '=', 'Administrator'), ('email', '!=', admin_user_email), ]
        user_id = ResUsers.browse(args).id

        if user_id != []:

            values = {
                'lang': self.lang,
                'tz': self.tz,
                'email': admin_user_email,
                'image_1920': Administrator_image,
            }
            ResUsers.write(user_id, values)

            group_name_list = [
                'Contact Creation',
            ]
            self.user_groups_setup('Administrator', group_name_list)

            print('Done.')

        else:

            print('User "{0}" already configured.'.format('Administrator'))
            # print('Done.')

    # def demo_user_setup(self, demo_user_name, demo_user_email, CompanyName, demo_user, demo_user_pw, Demo_User_image):

    #     print('Configuring user "Demo"...')

    #     client = erppeek.Client(
    #         server=self.server,
    #         db=self.dbname,
    #         user='admin',
    #         password=self.admin_user_pw)

    #     ResUsers = client.model('res.users')
    #     args = [('name', '=', demo_user_name), ]
    #     user = ResUsers.browse(args)

    #     if user.id == []:

    #         ResPartner = client.model('res.partner')
    #         args = [('name', '=', CompanyName), ]
    #         parent_id = ResPartner.browse(args).id

    #         ResCompany = client.model('res.company')
    #         args = [('name', '=', CompanyName), ]
    #         company_id = ResCompany.browse(args).id

    #         values = {
    #             'name': demo_user_name,
    #             # 'customer': False,
    #             'employee': False,
    #             'is_company': False,
    #             'email': demo_user_email,
    #             'website': '',
    #             'parent_id': parent_id[0],
    #             'company_id': company_id[0],
    #             'tz': self.tz,
    #             'lang': self.lang
    #         }
    #         partner_id = ResPartner.create(values)

    #         values = {
    #             'name': demo_user_name,
    #             'partner_id': partner_id,
    #             'company_id': company_id[0],
    #             'login': demo_user,
    #             'password': demo_user_pw,
    #             'image_1920': Demo_User_image,
    #         }
    #         ResUsers.create(values)

    #         print('Done.')

    #     else:

    #         print('User "{0}" already configured.'.format(demo_user_name))
    #         print('Done.')

    def data_administrator_user_setup(
        self, data_admin_user_name, data_admin_user_email, CompanyName,
        data_admin_user, data_admin_user_pw, DataAdministrator_image
    ):

        print('Configuring user "Data Administrator"...')

        client = erppeek.Client(
            server=self.server,
            db=self.dbname,
            user='admin',
            password=self.admin_user_pw)

        ResUsers = client.model('res.users')
        args = [('name', '=', data_admin_user_name), ]
        user = ResUsers.browse(args)

        if user.id == []:

            ResPartner = client.model('res.partner')
            args = [('name', '=', CompanyName), ]
            parent_id = ResPartner.browse(args).id

            ResCompany = client.model('res.company')
            args = [('name', '=', CompanyName), ]
            company_id = ResCompany.browse(args).id

            values = {
                'name': data_admin_user_name,
                # 'customer': False,
                'employee': False,
                'is_company': False,
                'email': data_admin_user_email,
                'website': '',
                'parent_id': parent_id[0],
                'company_id': company_id[0],
                'tz': self.tz,
                'lang': self.lang
            }
            partner_id = ResPartner.create(values)

            values = {
                'name': data_admin_user_name,
                'partner_id': partner_id,
                'company_id': company_id[0],
                'login': data_admin_user,
                'password': data_admin_user_pw,
                'image_1920': DataAdministrator_image,
            }
            ResUsers.create(values)

            print('Done.')

        else:

            print('User "{0}" already configured.'.format(data_admin_user_name))
            # print('Done.')

    def user_groups_setup(self, user_name, group_name_list):

        print('Executing user_groups_setup...')

        client = erppeek.Client(
            server=self.server,
            db=self.dbname,
            user='admin',
            password=self.admin_user_pw)

        ResUsers = client.model('res.users')
        args = [('name', '=', user_name), ]
        user_id = ResUsers.browse(args).id

        ResGroups = client.model('res.groups')

        for group_name in group_name_list:
            args = [('name', '=', group_name)]
            group_id = ResGroups.browse(args).id
            if group_id != []:
                values = {
                    'groups_id': [(4, group_id[0])],
                }
                ResUsers.write(user_id, values)

        # print('Done.')
        print('Done (user_groups_setup).')

    def module_install_upgrade(self, module_name, upgrade=False):

        print('Module Name: "{0}" (Update: {1})'.format(module_name, upgrade))

        client = erppeek.Client(
            server=self.server,
            db=self.dbname,
            user='admin',
            password=self.admin_user_pw)

        modules = client.modules()
        if module_name in modules['uninstalled']:
            print('Installing module "{0}"...'.format(module_name))
            client.install(module_name)
            print('Done.')
            return True

        elif upgrade:
            print('Upgrading module "{0}"...'.format(module_name))
            client.upgrade(module_name)
            print('Done.')
            return True

        else:
            print('Skipping module "{0}"...'.format(module_name))
            print('Done.')
            return False
