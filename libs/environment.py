__author__ = 'jon'

import logging
import ConfigParser

log = logging.getLogger()


class Environment(object):
    def __init__(self, ini_file):
        self.config = self._read_config(ini_file)
        self.settings = dict()
        self._config_to_settings()

    def getSetting(self, key):
        try:
            return self.settings[key]
        except KeyError:
            log.error('getSetting - Invalid key %s' % key)

    def setSetting(self, key, value):
        self.settings[key] = value

    def _read_config(self, ini_file):
        config = ConfigParser.ConfigParser()
        config.read("ini_files/%s" % ini_file)
        return config

    def _get_config_value(self, parent, key):
        try:
            return self.config.get(parent, key)
        except:
            log.error("INI Error: %s section missing %s key" % (parent, key))
            print "Job Manager Server aborted during config - INI file not correct, check log for details"
            exit()

    def _config_to_settings(self):
        # job manager specific settings
        self.setSetting('port', self._get_config_value('job_manager', 'port'))
        self.setSetting('auth_key', self._get_config_value('job_manager', 'auth_key'))
        # mail specific settings
        self.setSetting('mailserver', self._get_config_value('mail', 'server'))
        # database specifc settings
        self.setSetting('dbhost', self._get_config_value('database', 'dbhost'))
        self.setSetting('database', self._get_config_value('database', 'database'))
        self.setSetting('dbuser', self._get_config_value('database', 'dbuser'))
        self.setSetting('password', self._get_config_value('database', 'password'))