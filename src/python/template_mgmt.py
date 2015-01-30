'''
Created on 2013-11-30

'''

import os
from bottle import request
from Cheetah.Template import Template

import logging 
logger = logging.getLogger("ops.template")  

class MyUserData():
    
    username = ""
    infoname = ""
    datatype = ""
    datainfo = ""
    def __init__(self):
        pass
         
    def __exit__(self):
        pass
            

def file_read_html(path):
    filepath="webapps/"+path
    print "open file: %s"%filepath   
    if os.path.isfile(filepath) == 0:
        print "the file %s does not exist"%filepath
        return
    if path.endswith('.db') == True:
        return ''
    file = open(filepath, "rb");    
    if file == None:
        print "open file %s failed"%filepath
        return
    content=file.read()      
    print "get file content OK"
    file.close()
    #print content    
    return content
    
def login_submit(path):     
    if path == 'dc/sdncui.html':        
        name     = request.forms.get('name')     
        password = request.forms.get('password')     
        if check_login(name, password):         
            filepath="webapps/"+path  
            print "open file: %s"%filepath      
            file = open(filepath, "rb");    
            if file == None:
                print "open file %s failed"%filepath
                return
            content=file.read()      
            print "get file content OK"
            file.close() 
            return content  
        else:         
            return "<p>Login failed</p>"  
    else:
        return
        
def check_login(name, password):     
    if name == 'root' and password == 'root':         
        return True 
    
def fileget_proc(path):
    return file_read_html(path)

def filepost_proc(path):
    return login_submit(path)
    
def webapp_general_process(path,method):
    if method == 'GET':
        ret = fileget_proc(path)
    elif method == 'POST':
        ret = filepost_proc(path)
    else:
        pass
    
    return ret

def getTemplatefileBypath(method, path): 
    
    app = path
    if path.find('?') != -1:
        temp = path.split('?')
        app=temp[0]
    
    templatefile='%s.tmpl' % app
    templatefile.replace('/', os.sep)
    prefixpath= 'template%s%s' %(os.sep, method)
    templatepath = os.path.join(os.getcwd(), prefixpath, templatefile)
    
    if not os.path.exists(templatepath):
        errormsg='fail to open file %s'  % path
        logger.debug('fail to open file %s ' % templatefile)   
        raise Exception(errormsg)
        
    return templatepath
 
def getuserinfoBypath(path):
    temp = path.split('?')
    templen = len(temp)
    userdata = MyUserData()
    userinfo = temp[templen-1]
    userinfo_temp = userinfo.split('&')
    datatype=''
    datainfo=''
    #print path
    for elem in userinfo_temp:
        elem_tmp = elem.split('=')
        if elem_tmp[0] == 'username':
            userdata.username=elem_tmp[1]
        if elem_tmp[0] == 'infoname':
            userdata.infoname=elem_tmp[1]
        if elem_tmp[0] == 'datatype':
            userdata.datatype=elem_tmp[1]
        if elem_tmp[0] == 'data':
            userdata.datainfo=elem_tmp[1]
    return userdata

def check_userPsd(inputPsd, storePsd):
    #print 'inputPsd',inputPsd
    #print 'storePsd',storePsd
    if inputPsd == storePsd:
        return True
    else:
        return False

def template_get(path):  
    
    #userdata = getuserinfoBypath(path)
    try:
        
        templatefile = getTemplatefileBypath('get', path)
        templateDef = open(templatefile).read()
        data = Template(templateDef, searchList=[{'user' : "xxxxx",
                                        'order' : 'eeeee', 'name': "xxx"}])
        
        retData = '%s' %data 
        return retData
    
    except Exception as e:
        return '<error>%s<error>'%e

def template_post(path,body):
    userdata = getuserinfoBypath(path)    
     
    if body == None or body == '':
        body =userdata.datainfo
    try:
        ##ret = dm.add_userdata(userdata.username,userdata.infoname,userdata.datatype,body)
        if ret == True:
            return '<ok></ok>'
    except Exception as e:
        return '<error>%s<error>'%e

def template_put(path,body):    
    userdata = getuserinfoBypath(path)    
     
    if body == None or body == '':
        body = userdata.datainfo
     
    try:
       ## ret = dm.update_userdata(userdata.username,userdata.infoname,userdata.datatype,body)
        if ret == True:
            return '<ok></ok>'
    except Exception as e:
        return '<error>%s<error>'%e

def template_delete(path):
    userdata = getuserinfoBypath(path)    
     
 
    try:
        #ret = dm.delete_userdata(userdata.username,userdata.infoname)
        if ret == True:
            return '<ok></ok>'
    except Exception as e:
        return '<error>%s<error>'%e

def ops_manager_process(path, method, body=None):
    if method == 'GET':
        ret = template_get(path)
    elif method == 'POST':
        ret = template_post(path,body)
    elif method == 'PUT':
        ret = template_put(path,body)
    elif method == 'DELETE':
        ret = template_delete(path)
    else:
        pass
    
    return ret


if __name__ == '__main__':
    ops_manager_process('dc?username=admin&infoname=userdata&datatype=password&data=admin', 'POST')
    ops_manager_process('dc?username=admin&infoname=userpage&datrdatype=data&data=xxxxxxxxxxxxx', 'POST')
    ret = ops_manager_process('dc?username=admin&infoname=userpage', 'GET')
    print ret
    ret = ops_manager_process('dc/checkresult?username=admin&infoname=userdata&data=abcd', 'GET')
    print ret    
    ret = ops_manager_process('dc/checkresult?username=admin&infoname=userdata&data=admin', 'GET')
    print ret
    
    