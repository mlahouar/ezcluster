

import os
import errno

def ERROR(err):
    print "* * * * ERROR: {}".format(err)
    #raise Exception("xx")
    exit(1)

def appendPath(p1, p2):
    if os.path.isabs(p2):
        return p2
    else:
        return os.path.normpath(os.path.join(p1, p2))


def ensureFolder(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
        else:
            pass


def locate(key, dict1, dict2, errmsg):
    if key in dict1:
        return dict1[key]
    else:
        if key in dict2:
            return dict2[key]
        else:
            ERROR(errmsg)
                

def setDefaultInMap(root, key, defaultValue):
    if not key in root:
        root[key] = defaultValue

def findUpward(fileName, path):
    return findUpward2(fileName, path, path, 0)
 
def findUpward2(fileName, initial, location, cpt):
    x = os.path.join(location , fileName)
    if os.path.isfile(x):
        # Found !
        return x
    else:
        if location == "" or location == "/" :
            ERROR("Unable to locate a {0} file in '{1}' and upward".format(fileName, initial))
        else:
            if cpt < 30:
                return findUpward2(fileName, initial, os.path.dirname(location), cpt + 1)
            else:
                raise Exception("Too many lookup while trying to locate '{}'".format(fileName))

REPOSITORIES="repositories"

def lookupRepository(model, token):
    setDefaultInMap(model["data"], "repositories", {})
    repoId = model["cluster"][token]["repo_id"] # Should be Required by schema
    if REPOSITORIES not in model["config"] or token not in model["config"][REPOSITORIES]:
        ERROR("Missing {}.{} in configuration file".format(REPOSITORIES, token))
    #print model["config"][REPOSITORIES][token]
    l = filter(lambda x: x["repo_id"] == repoId, model["config"][REPOSITORIES][token])
    if len(l) > 1:
        ERROR("{} repo_id '{}' is defined twice in configuration file!".format(token, repoId))
    if len(l) != 1:
        ERROR("{} repo_id '{}' is not defined in configuration file!".format(token, repoId))
    model["data"][REPOSITORIES][token] = l[0]
    
