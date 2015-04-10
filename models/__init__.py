# -*- coding:utf-8 -*-
import os

for root, directory_names, file_names in os.walk('palvin/models'):
    for filename in file_names:
        split_filename = filename.split('.')
        if split_filename[-1] == 'py' and filename != '__init__.py':
            modname = '%s.%s' % (root.replace('/', '.'), split_filename[0])
            print "* Import %s..." % modname,
            try:
                module = __import__(modname, globals=globals(), locals=locals(), fromlist=['*'])
            except ImportError:
                continue
            else:
                for object_ in dir(module):
                    locals()[object_] = getattr(module, object_)
                print 'Done'