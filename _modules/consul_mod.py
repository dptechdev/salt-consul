# -*- coding: utf-8 -*-
'''
Execution module to provide consul functionality to Salt

.. versionadded:: 2014.7.0

:configuration: This module requires the python-consul python module and uses the
    following defaults which may be overridden in the minion configuration:

.. code-block:: yaml

    consul.host: 'localhost'
    consul.port: 8500
    consul.token: None
    consul.consistency: 'default'
'''

# Import third party libs
try:
    import consul as consul
    HAS_CONSUL = True
except ImportError:
    HAS_CONSUl = False

__virtualname__ = 'consul'


def __virtual__():
    '''
    Only load this module if consul python module is installed
    '''
    if HAS_CONSUL:
        return __virtualname__
    else:
        return False


def _connect(host='localhost', port=8500, consistency='default'):
    '''
    Returns an instance of the consul client
    '''
    if not host:
        host = __salt__['config.option']('consul.host')
    if not port:
        port = __salt__['config.option']('consul.port')
    if not consistency:
        consistency = __salt__['config.option']('consul.consistency')
    return consul.Consul(host, port, consistency)

def key_delete(key, recurse=None):
    '''
    Deletes the keys from consul, returns number of keys deleted

    CLI Example:

    .. code-block:: bash

        salt '*' consul.delete foo
    '''
    # Get connection args from keywords if set

    c = _connect()
    index, data = c.kv.get(key)
    if not data:
        return False
    else:
        return c.kv.delete(key, recurse)



def key_exists(key):
    '''
    Return true if the key exists in consul

    CLI Example:

    .. code-block:: bash

        salt '*' consul.exists foo
    '''
    c = _connect()
    index, data = c.kv.get(key)
    if not data:
        return False
    else:
        return True
        

def key_get(key):
    '''
    Gets the value of the key in consul

    CLI Example:

    .. code-block:: bash

        salt '*' consul.exists foo
    '''
    c = _connect()
    index, data = c.kv.get(key)
    if not data:
        return False
    else:
        return data['Value']


def key_put(key, value):
    '''
    Sets the value of a key in consul

    CLI Example:

    .. code-block:: bash

        salt '*' consul.exists foo
    '''
    c = _connect()
    c.kv.put(key, value)
    index, data = c.kv.get(key)
    return data['Value']

