# encoding: UTF-8
#-*-coding:utf-8-*-
import os
from PIL import Image


image_dic = {
    'png':'image/png',
    'jpg':'image/jpeg',
    'jpeg':'image/jpeg',
    'bmp':'image/bmp',
}

class CreateHtmlClass:
    """docstring for CreateHtml"""
    def __init__(self):
        self.root = "."

#    def check_image(self,path):
#        type_pos = path.rfind('.')
#        type_str = path[type_pos+1:]
#        if not image_dic.has_key( type_str.lower() ):
#            return False,0
#
#        im = Image.open(path)
#        width = im.size[0]
#        height = im.size[1]
#        ratio = width/1400.0
#        if  ratio > 1.0 :
#            return True,str(int(height/ratio))
#        else:
#            return False,1
    def check_image(self,path):
        type_pos = path.rfind('.')
        type_str = path[type_pos+1:]
        if not image_dic.has_key( type_str.lower() ):
            return False,0
        try:
            im = Image.open(path)
            width = im.size[0]
            height = im.size[1]
            ratio = width/1400.0
            if  ratio > 1.0 :
                return True,str(int(height/ratio))
            else:
                return False,1
        except Exception, e:
            print e
            return False,1
        
    def creat_dir_html(self,path):
        if path == '/':
            path = ""
        local_path = self.root + path
        content = ""
        local_path_about = local_path + '/about.info'
        if os.path.exists(local_path_about):
            f = open(local_path_about,'r')
            h2 = f.readline()
            f.close()

            content = '<title>Directory listing for '+ h2+'</title><body><center><h2>'+ h2 +'</h2><hr><ul>'
            for f in os.listdir(local_path):
                if str(f) != 'about.info':
                    is_image,height = self.check_image(local_path + '/' + str(f))
                    if is_image:
                        content += '<li style=" list-style:none"><img src="' + path + '/' + str(f) + '" alt="' + str(f) + '" width="1400" height="'+ height +'"/></li><br/><br/>'
                    elif height == 1:
                        content += '<li style=" list-style:none"><img src="' + path + '/' + str(f) + '" alt="' + str(f) + '" /></li><br/><br/>'
            content += '</ul></center><hr></body></html>'
        else:
            content = '<title>Directory listing for '+ path+'</title><body><h2>'+ path +' /</h2><hr><ul>'
            for f in os.listdir(local_path):
                content += '<li><a href="' + path + '/' + str(f) + '">' + str(f) + '</a></li>'
            content += '</ul><hr></body></html>'
        return content

    def read_local_file(self,path):
        f = open(path,'rb')
        read = f.read()
        f.close()
        #print path
        return read

    def write_local_file(self,path,content):
        f = open(path,'w')
        f.write(content)
        f.close()

    def get_dir_html(self,path,refresh_pos):
        content = None
        content_type = None
        error_code = 200
        local_path = self.root + path
        path_name_pos = path.rfind('/')
        path_name = path[path_name_pos+1:]
        local_path_html = local_path + '/'+path_name+'.html'
        print local_path_html
        content_type = "text/html; charset=utf-8"
        if path == '/' :
            content = self.creat_dir_html(path)
#        elif refresh_pos == -1 and os.path.exists(local_path_html):
#            content = self.read_local_file(local_path_html)
        else:
            content = self.creat_dir_html(path)
#            self.write_local_file(local_path_html,content)

        return error_code,content_type,content

    def get_404_html(self):
        content = "404"
        error_code = 404
        content_type = "text/html; charset=utf-8"
        return error_code,content_type,content

    def get_file_content(self,path):
        if path=='/':
            path = ""
        local_path = self.root + path
        type_pos = path.rfind('.')
        type_str = path[type_pos+1:]
        content_type = "*/*"
        print type_str
        error_code = 200
        if image_dic.has_key(type_str.lower()):
            content_type = image_dic[type_str.lower()]

        if os.path.exists(local_path):
            content = self.read_local_file(local_path)
        else:
            return self.get_404_html()
        return error_code,content_type,content

    def root_html(self,path):
        refresh_pos = path.find('refresh')
        if refresh_pos != -1:
            path = path[0:refresh_pos-1]
        content = None
        content_type = None
        error_code = None
        local_path = self.root + path

        
        if os.path.isdir(local_path):
            error_code,content_type,content = self.get_dir_html(path,refresh_pos)
        else:
            error_code,content_type,content = self.get_file_content(path)

        return error_code,content_type,content