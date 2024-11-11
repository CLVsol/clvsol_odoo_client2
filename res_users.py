# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

logging.basicConfig(level=logging.DEBUG)
_logger = logging.getLogger(__name__)


def res_user_migrate(
    rsock, ruid, remote_admin_user_pw, remote_dbname,
    lsock, luid, local_admin_user_pw, local_dbname
):

    remote_object_fields = ['id', 'name', 'partner_id', 'company_id', 'tz', 'lang',
                            'login', 'password', 'image', 'groups_id', 'active']

    remote_objects = rsock.execute(remote_dbname, ruid, remote_admin_user_pw,
                                   'res.users', 'search_read',
                                   [],
                                   remote_object_fields)

    _logger.info(u'%s %s\n', '--> remote_objects', len(remote_objects))

    local_object_fields = ['id', 'name', 'partner_id', 'company_id',
                           'login', 'password', 'image_1920', 'groups_id', 'active']

    local_objects = lsock.execute(local_dbname, luid, local_admin_user_pw,
                                  'res.users', 'search_read',
                                  [],
                                  local_object_fields)

    _logger.info(u'%s %s\n', '--> local_objects', len(local_objects))

    for remote_object in remote_objects:
        local_object = lsock.execute(local_dbname, luid, local_admin_user_pw,
                                     'res.users', 'search_read',
                                     [('login', '=', remote_object['login'])],
                                     local_object_fields)
        _logger.info(u'%s %s', '-->', remote_object['name'])

        if local_object != []:
            _logger.info(u'%s %s', '----->', '*** Skipped ***')

        else:
            res_company = lsock.execute(local_dbname, luid, local_admin_user_pw,
                                        'res.company', 'search_read',
                                        [('name', 'in', remote_object['company_id'])],
                                        ['id'])
            company_id = res_company[0]['id']

            res_partner = lsock.execute(local_dbname, luid, local_admin_user_pw,
                                        'res.partner', 'search_read',
                                        [('name', 'in', remote_object['company_id'])],
                                        ['id'])
            parent_id = res_partner[0]['id']

            res_user_record = {}
            res_user_record['name'] = remote_object['name']
            res_user_record['login'] = remote_object['login']
            res_user_record['password'] = remote_object['password']
            if remote_object['image'] is not False:
                res_user_record['image_1920'] = remote_object['image']
            res_user_record['lang'] = remote_object['lang']
            res_user_record['tz'] = remote_object['tz']
            res_user_record['active'] = remote_object['active']
            user_id = lsock.execute(local_dbname, luid, local_admin_user_pw,
                                    'res.users', 'create',
                                    res_user_record)

            _logger.info(u'%s %s', '----->', user_id)

            res_user = lsock.execute(local_dbname, luid, local_admin_user_pw,
                                     'res.users', 'search_read',
                                     [('id', '=', user_id)],
                                     ['id', 'name', 'partner_id'])

            res_partner = lsock.execute(local_dbname, luid, local_admin_user_pw,
                                        'res.partner', 'search_read',
                                        [('name', 'in', res_user[0]['partner_id'])],
                                        ['id'])
            partner_id = res_partner[0]['id']

            _logger.info(u'%s %s', '----->', partner_id)

            res_partner_record = {}
            res_partner_record['email'] = remote_object['login']
            res_partner_record['parent_id'] = parent_id
            res_partner_record['company_id'] = company_id

            result = lsock.execute(local_dbname, luid, local_admin_user_pw,
                                   'res.partner', 'write',
                                   partner_id,
                                   res_partner_record)

            _logger.info(u'%s %s', '----->', result)
