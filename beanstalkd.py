#
# Plugin to collectd statistics from beanstalkd
#

import collectd

# beanstalkc needs yaml to work correctly.
# This import ensures a 'fail early' behaviour.
import yaml

from beanstalkc import Connection

class Beanstalk(object):

    def __init__(self):
        self.plugin_name = "beanstalkd"
        self.host = '127.0.0.1'
        self.port = 11300
        self.tubes_prefix = ['default']

    def submit(self, type, instance, value, tube=None):
        if tube:
            plugin_instance = '%s-%s' % (self.port, tube)
        else:
            plugin_instance = str(self.port)

        v = collectd.Values()
        v.plugin = self.plugin_name
        v.plugin_instance = plugin_instance
        v.type = type
        v.type_instance = instance
        v.values = [value, ]
        v.dispatch()

    def do_server_status(self):
        conn = Connection(self.host, self.port)
        srv_stats = conn.stats()

        for cmd in ('put', 'reserve-with-timeout', 'delete'):
            self.submit('counter', cmd, srv_stats['cmd-%s' % cmd])
        self.submit('counter', 'total_jobs', srv_stats['total-jobs'])
        for tube in conn.tubes():
            for prefix in self.tubes_prefix:
                if tube.startswith(prefix):
                    tube_stats = conn.stats_tube(tube)
                    self.submit('records', 'current_ready', tube_stats['current-jobs-ready'], tube)
                    self.submit('counter', 'total_jobs', tube_stats['total-jobs'], tube)

        conn.close()

    def config(self, obj):
        for node in obj.children:
            if node.key == 'Port':
                self.port = int(node.values[0])
            elif node.key == 'Host':
                self.host = node.values[0]
            elif node.key == 'tubes_prefix':
                self.tubes_prefix = node.values
            else:
                collectd.warning("beanstalkd plugin: Unkown configuration key %s" % node.key)

beanstalkd = Beanstalk()
collectd.register_read(beanstalkd.do_server_status)
collectd.register_config(beanstalkd.config)
