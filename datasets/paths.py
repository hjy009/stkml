import os


def path_root(child='datas'):
    # path = os.path.join(os.path.expanduser('~'), child)
    path = os.path.join('..', child)
    return path


def path1(child='tushare'):
    path = path_root()
    path = os.path.join(path, child)
    return path


def path1f(fname, hz='.csv'):
    path = path1()
    path = os.path.join(path, fname + hz)
    return path


def pathapi(api):
    path = path1f(api)
    return path


def path2(child):
    path = path1()
    path = os.path.join(path, child)
    return path


def path2f(child, fname):
    path = path2(child)
    path = os.path.join(path, fname + '.csv')
    return path

def pathapi2(child,fname):
    path = path2f(child, fname)
    return path

def path3(childs):
    path = path1()
    for i in range(len(childs)):
        path = os.path.join(path, childs[i])
    return path

def path3f(childs, fname):
    path = path3(childs)
    path = os.path.join(path, fname + '.csv')
    return path

def pathapi3(childs,fname):
    path = path3f(childs,fname)
    return path

def get_infopath():
    path = pathapi('infomation')
    return path

def get_dailypath(ts_code):
    path = pathapi2('daily',ts_code)
    return path

def get_barpath(ts_code,adj='qfq'):
    path = pathapi3(['bar',adj],ts_code)
    return path

