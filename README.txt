# Integrate it like this
<Plugin python>
    ModulePath "..../collectd_plugins/beanstalkd"
    Import "beanstalkd"
    <Module beanstalkd>
        Host "127.0.0.1"
        Port "11300"
        # only monitor tubes where tubename start with the following prefixes
        tubes_prefix "inventory default"
    </Module>
</Plugin>

You need
* https://pypi.python.org/pypi/beanstalkc
* https://pypi.python.org/pypi/PyYAML
