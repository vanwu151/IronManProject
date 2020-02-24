# coding=utf-8
import os, re
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.auth.hashers import make_password, check_password
from .models import upload as up
# Create your views here.


#def redirectlogin(requset):
#    request.session.clear()         #删除session里的全部内容
#    return redirect('/login')       #重定向到/login前端页面

def relogin(request):
    if request.method == "GET":
        return render(request, 'FinaceNote/Login.html')

def uploader(request):
    try:
        if request.method == "GET":
            filenoteinfo = '注意：上传的文件名中请勿包含空格！'
            return render(request, 'FinaceNote/upload.html',{'userinfo':{'filenoteinfo': filenoteinfo}})
        elif request.method == "POST":
            v1=request.POST.get('user')                                                              #获取前端login页面输入的用户名赋给变量v1
            # print(v1, type(v1))
            try:                                                                    
                j = up.objects.get( user_name = v1 ).user_name                                       #尝试通过前端login页面获取的用户名从数据库里查询有无记录
                print(j, type(j))
                info = v1 + ':该用户名已被注册！'                                                      #获取到记录则不会抛出异常，回传给前端Info信息，已查询到相同用户名的用户并提醒该用户名已被注册
                return render(request, 'FinaceNote/upload.html', {'userinfo': {'info': info}})
            except:                                                                                  #如果程序抛出异常则代表前端login页面获取的用户名在已有数据库里未查询到记录
                v2 = request.POST.get('gender')                                                      #可继续往下进行用户注册操作
                print(v2, type(v2))
                v3 = request.POST.getlist('favor')
                i = len(v3)
                v3all = ''
                for z in range(0, i):
                    v3all = v3all + v3[z] + " "
                print(v3all, type(v3))
                v4 = request.POST.getlist('city')[0]
                print(v4, type(v4))
                v5 = request.POST.get('pwd')
                password = make_password(v5,None,'pbkdf2_sha256')
                v6 = request.POST.get('nickname')
                os.mkdir("/opt/djangoproject/IronManProject/FinaceNote/upload/{}".format(v1))
                obj_file = request.FILES.getlist('upnewfile')    #获取前端传递来的文件列表 obj_file 二进制源码
                print(obj_file)          
                filenamelist = []
                info = '恭喜！ ' + v1 + ' 用户注册成功！'
                spacetest = re.compile(r"\s+")               # 文件名是否有空格监测正则 
                dottest = re.compile(r",")                   # 文件名是否有英文逗号监测正则                   
                for f in obj_file:                                
                    filename = f.name.replace("'","").replace(' ','')      # 根据文件列表获取文件名列表 filenamelist    
                    dot = dottest.findall(filename)
                    if dot:
                        filename = f.name.replace(",","，")   #如果有英文逗号则替换成中文逗号
                    space = spacetest.findall(filename)
                    if space:                                 #如果在文件名中匹配到空格
                        info = '账号注册成功，但文件名含有空格未上传！'
                        pass
                    else:                      
                        filenamelist.append(filename)
                # filenamelist.remove('')
                print(filenamelist)
                # print(obj, type(obj), obj.name)
                filepathlist = []    
                for fn in filenamelist:                      # 根据文件名列表 filenamelist创建下载文件的绝对路径列表 filepathlist
                    file_path = os.path.join("/opt/djangoproject/IronManProject/FinaceNote/upload/{}".format(v1), fn)
                    filepathlist.append(file_path)
                print(filepathlist)
                try:
                    for fp,obj in zip(filepathlist, obj_file):   # 将下载文件的绝对路径列表 filepathlist 与前端传递来的文件列表 obj_file 二进制源码，打包合并为下载信息列表
                        f = open(fp, mode="wb")                  # 遍历打包合并的文件下载信息列表，开始下载文件
                        for i in obj.chunks():
                            f.write(i)
                        f.close()
                except:
                    pass
                q = up(user_name = v1, user_sex = v2, user_hobby = v3, user_city = v4, user_filename = filenamelist, user_password = password, user_nickname = v6)
                q.save()
            return render(request, 'FinaceNote/Login.html', {'userinfo': {'info': info}})   #注册成功返回到登录页面
    except:
        info = '请填写注册信息！'
        return render(request, 'FinaceNote/upload.html', {'userinfo': {'info': info}})
    
def login(request):
    if request.method == "GET":
        return render(request, 'FinaceNote/Login.html')

def logout(request):                #注销操作 
    request.session.clear()         #删除session里的全部内容
    return redirect('/login')       #重定向到/login前端页面
    

def logininfo(request):
    if request.method == "POST":
        try:
            UserName=request.POST.get('user')
            UserPass=request.POST.get('pwd')
            # print(UserPass)
            tt = up.objects.get(user_name=UserName)
            name = tt.user_name
            pwd  = tt.user_password
            print(check_password(UserPass,pwd))
            if UserName == name and check_password(UserPass,pwd) is True:
                request.session['username'] = UserName    #定义session“username”字段并令session中username字段值为登录的用户名
                request.session['is_login'] = True        #定义session“is_login”字段并令该字段值为"True"表示会话已经创建
                ad = tt.user_role
                print(ad , type(ad))
                if ad == 'admin':
                    info = '欢迎您，管理员！'
                    userrole = '管理员'
                    return render(request, 'FinaceNote/showadmininfo.html', {'userinfo': {'info': info, 'name': name, 'userrole':userrole}})
                nickname = tt.user_nickname
                sex = tt.user_sex
                hobby = tt.user_hobby
                city = tt.user_city
               # filenamelist = tt.user_filename.replace('[', '').replace(']', '').replace("'","").replace(' ','')            #从数据库获取文件名字段类型为‘str’，做字符串过滤掉“[”，“]”，“'”不需要的字符，去掉文件名前的空格
                
               # filenamelistnew = filenamelist.split(',')                                                                    #根据过滤后的字符串 filenamelist生成文件名列表filenamelistnew
               # try:                                          # 如果之前上传过带空格文件名的文件filenamelistnew列表中会带出''元素所以需要删除从数据库获取的空字符串，转换成列表的''元素
                    #filenamelistnew.remove('')                # 列表中没有''元素时删除会报错
                #except:
                #    pass
                #print(filenamelistnew, type(filenamelistnew))
                #url_list=[]
                #fileindexlist = []
                #fileindex = 1
                #for url_name in filenamelistnew:
                #    fileindexlist.append(str(fileindex))
                #    filePath = "http://218.94.64.98:60097" + "/" + name + "/" + url_name     
                #    print(filePath)
                #    url_list.append(filePath)
                #    fileindex += 1
                #fileinfolist = zip(filenamelistnew, url_list, fileindexlist)
                return render(request, 'FinaceNote/showinfo.html', {'userinfo': {'name': request.session['username'], 'nickname':nickname, 'sex': sex, 'hobby': hobby, 'city':city}})
            else:
                info = '用户名或密码错误！'
                return render(request, 'FinaceNote/Login.html', {'userinfo': {'info': info}})
        except:
            info = '登录信息不能为空！'
            return render(request, 'FinaceNote/Login.html', {'userinfo': {'info': info}})

def myfiles(request):
    if request.session.get('is_login',None):
        if request.method == "GET":
            name = request.session['username']
            try:
                q = up.objects.get( user_name = name )
                filenamelist = q.user_filename.replace('[', '').replace(']', '').replace("'","").replace(' ','')            #从数据库获取文件名字段类型为‘str’，做字符串过滤掉“[”，“]”，“'”不需要的字符
                filenamelistnew = filenamelist.split(',')                                                    #根据过滤后的字符串 filenamelist生成文件名列表filenamelistnew
                try:                                                                                         # 如果之前上传过带空格文件名的文件filenamelistnew列表中会带出''元素所以需要删除从数据库获取的空字符串，转换成列表的''元素
                    filenamelistnew.remove('')
                except:
                    pass
                print(filenamelistnew, type(filenamelistnew))
                url_list=[]
                fileindexlist = []
                fileindex = 1
                for url_name in filenamelistnew:
                    fileindexlist.append(str(fileindex))
                    filePath = "http://218.94.64.98:60097" + "/" + name + "/" + url_name     #去掉文件名前的空格
                    url_list.append(filePath)
                    fileindex += 1
                fileinfolist = zip(filenamelistnew, url_list, fileindexlist)
                return render(request, 'FinaceNote/showfilesinfo.html', {'userinfo': {'name': name, 'fileinfolist':fileinfolist}})
            except:
                pass


def Userfiledel(request): 
    '''
    用户文件自主勾选删除功能
    '''
    if request.session.get('is_login',None):
        if request.method == "POST":
            UserName = request.session['username']
            try:
                tt = up.objects.get(user_name=UserName)
                #nickname = tt.user_nickname
                #sex = tt.user_sex
                #hobby = tt.user_hobby
                #city = tt.user_city
                filenamelist = tt.user_filename.replace('[', '').replace(']', '').replace("'","").replace(' ','')            #从数据库获取文件名字段类型为‘str’，做字符串过滤掉“[”，“]”，“'”不需要的字符，去掉文件名前的空格
                filenamelistnew = filenamelist.split(',')
                EditFilesName = request.POST.getlist('files')                                                                #从前端获取需要删除的文件名列表 EditFilesName
                action = request.POST.get('action')
                if action:
                    print(EditFilesName)
                    dirpath = "/opt/djangoproject/IronManProject/FinaceNote/upload/{}".format(UserName)
                    for files in EditFilesName:                                                                              #从文件名列表 EditFilesName 遍历需要删除的文件名 files
                        file_path = os.path.join(dirpath, files)                                                
                        os.remove(file_path)                                                                                 #根据文件名 files + 用户文件路径 删除文件
                        print(files)
                        filenamelistnew.remove(files)                                                                        #在当前用户数据库获取过滤后的filenamelistnew文件名列表中删除 files 元素
                    print(filenamelistnew)
                    try:
                        filenamelistnew.remove('')
                    except:
                        pass
                    tt.user_filename = filenamelistnew                                                                       #更新用户user_filename字段，值为删除files元素的filenamelistnew
                    tt.save()
                    url_list=[]
                    fileindexlist = []
                    fileindex = 1
                    for url_name in filenamelistnew:
                        fileindexlist.append(str(fileindex))
                        filePath = "http://218.94.64.98:60097" + "/" + UserName + "/" + url_name
                        url_list.append(filePath)
                        fileindex += 1
                    fileinfolist = zip(filenamelistnew, url_list, fileindexlist)
            except:
                pass
            return render(request, 'FinaceNote/showfilesinfo.html', {'userinfo': {'name': request.session['username'], 'fileinfolist':fileinfolist}})

def SearchFiles(request): 
    '''
    用户搜索文件功能
    '''
    if request.session.get('is_login',None):
        if request.method == "POST":           
            UserName = request.session['username']
            try:
                tt = up.objects.get(user_name=UserName)
                filenamelist = tt.user_filename.replace('[', '').replace(']', '').replace("'","").replace(' ','')            #从数据库获取文件名字段类型为‘str’，做字符串过滤掉“[”，“]”，“'”不需要的字符，去掉文件名前的空格
                filenamelistnew = filenamelist.split(',')
                search = request.POST.get('search')
                go = request.POST.get('go')
                if go:
                    try:
                        filenamelistnew.remove('')
                    except:
                        pass
                    keyword = re.compile(r"{}".format(search))
                    searchResault = []
                    try:
                        for filename in filenamelistnew:
                            if keyword.findall(filename):     #如果文件名中有关键字
                                searchResault.append(filename)
                    except:
                        pass
                    url_list=[]
                    fileindexlist = []
                    fileindex = 1
                    for url_name in searchResault:
                        fileindexlist.append(str(fileindex))
                        filePath = "http://218.94.64.98:60097" + "/" + UserName + "/" + url_name
                        url_list.append(filePath)
                        fileindex += 1
                    fileinfolist = zip(searchResault, url_list, fileindexlist)
            except:
                pass
            return render(request, 'FinaceNote/showfilesinfo.html', {'userinfo': {'name': request.session['username'], 'fileinfolist':fileinfolist}})

def Useruploadfile(request):
    '''
    用户文件自主上传文件功能
    '''
    if request.session.get('is_login',None):
        if request.method == "POST":
            UserName = request.session['username']
            try:
                tt = up.objects.get(user_name=UserName)
                #nickname = tt.user_nickname
                #sex = tt.user_sex
                #hobby = tt.user_hobby
                #city = tt.user_city
                dirpath = "/opt/djangoproject/IronManProject/FinaceNote/upload/{}".format(UserName)
                filenamelist = tt.user_filename.replace('[', '').replace(']', '').replace("'","").replace(' ','')            #从数据库获取文件名字段类型为‘str’，做字符串过滤掉“[”，“]”，“'”不需要的字符，去掉文件名前的空格
                filenamelistnew = filenamelist.split(',')
                obj_file = request.FILES.getlist('upnewfile')
                action = request.POST.get('action')
                spacetest = re.compile(r"\s+")               # 文件名空格监测正则
                dottest = re.compile(r",")                   #如果有英文逗号则替换成中文逗号
                if action:
                    newfiles_pathlist = []                        #新增文件的绝对文件路径列表
                    for f in obj_file:                            #根据文件列表获取文件名列表 filenamelist
                        filename = f.name
                        dot = dottest.findall(filename)
                        if dot:
                            filename = filename.replace(",","，")   #如果有英文逗号则替换成中文逗号
                        space = spacetest.findall(filename)         #查找上传的文件名中包含空格space
                        if space:                                 #如果有空格
                            pass                                  #则不对文件列表 filenamelistnew更新 直接跳过该步
                        else:
                            filename = filename.replace("'","").replace(' ','')
                            # print(f.name)
                            if filename in filenamelistnew:           #判断上传的新文件名是否在已存在的用户文件列表 filenamelistnew中
                                pass
                            else:                                     #如果不在则继续执行文件列表 filenamelistnew 与下载文件的绝对路径列表 newfiles_pathlist 的更新
                                filenamelistnew.append(filename)
                                file_path = os.path.join(dirpath, filename)
                                newfiles_pathlist.append(file_path)
                    try:                                               # 如果之前上传过带空格文件名的文件filenamelistnew列表中会带出''元素所以需要删除从数据库获取的空字符串，转换成列表的''元素
                        filenamelistnew.remove('')
                    except:
                        pass
                    print(filenamelistnew)
                    print(newfiles_pathlist)
                    for fp,obj in zip(newfiles_pathlist, obj_file):   # 将新增下载文件的绝对路径列表 newfiles_pathlist 与前端传递来的文件列表 obj_file 二进制源码，打包合并为下载信息列表
                        f = open(fp, mode="wb")                       # 遍历打包合并的文件下载信息列表，开始下载文件
                        for i in obj.chunks():
                            f.write(i)
                        f.close()
                    tt.user_filename = filenamelistnew
                    tt.save()                    
                    url_list=[]
                    fileindexlist = []
                    fileindex = 1
                    for url_name in filenamelistnew:
                        fileindexlist.append(str(fileindex))
                        filePath = "http://218.94.64.98:60097" + "/" + UserName + "/" + url_name
                        url_list.append(filePath)
                        fileindex += 1
                    fileinfolist = zip(filenamelistnew, url_list, fileindexlist)                    
            except:
                pass
            return render(request, 'FinaceNote/showfilesinfo.html', {'userinfo': {'name': request.session['username'], 'fileinfolist':fileinfolist}})

                
def modinfo(request):
    if request.session.get('is_login',None):
        if request.method == "POST":
            name = request.session['username']
            try:
                nickname = up.objects.get( user_name = name).user_nickname
            except:
                pass
            return render(request, 'FinaceNote/Modinfo.html', {'userinfo': {'name': name, 'nickname': nickname}})

def InfoModed(request):
    if request.session.get('is_login',None):
        if request.method == "POST":        
            try:
                m = request.session['username']     #从session中获取用户姓名
                p = request.POST.get('passwd')      #获取前端输入的密码赋给变量p
                q = up.objects.get(user_name=m)     #以查询条件q：字段user_name值为cookie重保存的用户信息为条件
                p2 = q.user_password                #通过查询条件q将用户的密码赋给变量p2
                if check_password(p,p2) is True:                               #当输入的密码p和查询出的密码p2比较后为真       
                    info = m + '信息更改成功！'
                    name = q.user_name                                         #将回传给前端的name字段赋值为通过查询条件q查到的用户名
                    ModPwd = request.POST.get('userinfo_passwd')
                    if ModPwd != '':
                        NewPwd = make_password(ModPwd ,None, 'pbkdf2_sha256')
                        q.user_password = NewPwd
                        q.save()
                        info = m + '密码已更改！'
                    else:
                        pass
                    ModNickName = request.POST.get('userinfo_nickname')        #获取前端输入的新昵称赋给变量ModNickName
                    if ModNickName != '':                                      #如果获取到的新昵称值不是空的
                        q.user_nickname = ModNickName                          #则将变量ModNickName新昵称，更新到数据库user_nickname字段
                        q.save()                                               #保存更新
                        nickname = q.user_nickname                             #将回传给前端的nickname字段赋值为通过查询条件q查到的昵称
                    else:                                                      #如果获取到的新昵称是空的
                        nickname = q.user_nickname                             #则不去更新数据库
                    ModSex = request.POST.get('userinfo_sex')
                    if ModSex != None:
                        q.user_sex = ModSex
                        q.save()
                        sex = q.user_sex
                    else:
                        sex = q.user_sex
                    ModHobbyList = request.POST.getlist('userinfo_hobby')
                    i = len(ModHobbyList)
                    ModHobby = ''
                    for z in range(0, i):
                        ModHobby = ModHobby + ModHobbyList[z] + " "
                    if ModHobby != '':
                        q.user_hobby = ModHobby
                        q.save()
                        hobby = q.user_hobby
                    else:
                        hobby = q.user_hobby
                    ModCityList = request.POST.getlist('userinfo_city')
                    print(ModCityList, type(ModCityList))
                    if len(ModCityList) >= 1:
                        q.user_city = ModCityList[0]
                        q.save()
                        city = q.user_city
                    else:
                        city = q.user_city
                    #filenamelist = q.user_filename.replace('[', '').replace(']', '').replace("'","").replace(' ','')            #从数据库获取文件名字段类型为‘str’，做字符串过滤掉“[”，“]”，“'”不需要的字符
                    #filenamelistnew = filenamelist.split(',')                                                    #根据过滤后的字符串 filenamelist生成文件名列表filenamelistnew
                    #try:
                    #    filenamelistnew.remove('')
                    #except:
                    #    pass
                    #print(filenamelistnew, type(filenamelistnew))
                    #url_list=[]
                    #fileindexlist = []
                    #fileindex = 1
                    #for url_name in filenamelistnew:
                    #    fileindexlist.append(str(fileindex))
                    #    filePath = "http://218.94.64.98:60097" + "/" + name + "/" + url_name     #去掉文件名前的空格
                    #    url_list.append(filePath)
                    #    fileindex += 1
                    #fileinfolist = zip(filenamelistnew, url_list, fileindexlist)
                    return render(request, 'FinaceNote/showinfo.html', {'userinfo': {'info': info,'name': name, 'nickname':nickname, 'sex': sex, 'hobby': hobby, 'city':city}})
                elif check_password(p,p2) is False:
                    info = '密码错误！信息更改失败！'
                    name = q.user_name
                    nickname = q.user_nickname
                    return render(request, 'FinaceNote/Modinfo.html', {'userinfo': {'info': info,'name': name, 'nickname':nickname}})
                else:
                    info = '用户信息错误！信息更改失败！'
                    name = q.user_name
                    nickname = q.user_nickname
                    return render(request, 'FinaceNote/Modinfo.html', {'userinfo': {'info': info,'name': name, 'nickname':nickname}})
            except:
                info = '请填入正确的修改信息！'
                name = q.user_name
                nickname = q.user_nickname
                return render(request, 'FinaceNote/Modinfo.html', {'userinfo': {'info': info,'name': name, 'nickname':nickname}})

def viewinfo(request):
    if request.session.get('is_login',None):
        if request.method == "GET":
            name = request.session['username']
            try:
                q = up.objects.get( user_name = name )
                nickname = q.user_nickname
                sex = q.user_sex
                hobby = q.user_hobby
                city = q.user_city
                #filenamelist = q.user_filename.replace('[', '').replace(']', '').replace("'","").replace(' ','')            #从数据库获取文件名字段类型为‘str’，做字符串过滤掉“[”，“]”，“'”不需要的字符
                #filenamelistnew = filenamelist.split(',')                                                    #根据过滤后的字符串 filenamelist生成文件名列表filenamelistnew
                #try:                                                                                         # 如果之前上传过带空格文件名的文件filenamelistnew列表中会带出''元素所以需要删除从数据库获取的空字符串，转换成列表的''元素
                    #filenamelistnew.remove('')
                #except:
                    #pass
                #print(filenamelistnew, type(filenamelistnew))
                #url_list=[]
                #fileindexlist = []
                #fileindex = 1
                #for url_name in filenamelistnew:
                #    fileindexlist.append(str(fileindex))
                #    filePath = "http://218.94.64.98:60097" + "/" + name + "/" + url_name     #去掉文件名前的空格
                #    url_list.append(filePath)
                #    fileindex += 1
                #fileinfolist = zip(filenamelistnew, url_list, fileindexlist)
                return render(request, 'FinaceNote/showinfo.html', {'userinfo': {'name': name,'nickname':nickname,'sex': sex, 'hobby': hobby, 'city':city}})
            except:
                pass

def Manage(request):
    if request.session.get('is_login',None):
        if request.method == "POST" or request.method == "GET":
            try:
                # info = '用户管理列表'
                m = request.session['username']
                userdic = up.objects.exclude(user_name = m).exclude(user_name = "admin")
                userlist = []
                rolelist = []
                for i in userdic:
                    userlist.append(i)
                print(userlist)
                for k in userlist:
                    q = up.objects.get(user_name = k)
                    role = q.user_role
                    rolelist.append(role)
                print(rolelist)
                userroleinfolist=zip(userlist,rolelist)                    #将userlist与rolelist打包成userroleinfolist
                return render(request, 'FinaceNote/Manage.html', {'userinfo': {'name': m, 'userroleinfolist': userroleinfolist}})
            except:
                pass


def Edit(request):
    if request.session.get('is_login',None):
        if request.method == "POST":
            EditUserName = request.POST.get('username')
            request.session['EditUserName'] = EditUserName                              #定义session“EditUserName”字段并令session中EditUserName字段值为需要编辑的用户名
            print(EditUserName)
            action = request.POST.get('action')
            try:
                try:
                    if action == "编辑":
                        q = up.objects.get(user_name = EditUserName)
                        name = q.user_name
                        nickname = q.user_nickname
                        sex = q.user_sex
                        hobby = q.user_hobby
                        city = q.user_city
                        filenamelist = q.user_filename.replace('[', '').replace(']', '').replace("'","").replace(' ','')            #从数据库获取文件名字段类型为‘str’，做字符串过滤掉“[”，“]”，“'”不需要的字符
                        filenamelistnew = filenamelist.split(',')                                                    #根据过滤后的字符串 filenamelist生成文件名列表filenamelistnew
                        try:                                                                                         # 如果之前上传过带空格文件名的文件filenamelistnew列表中会带出''元素所以需要删除从数据库获取的空字符串，转换成列表的''元素
                            filenamelistnew.remove('')
                        except:
                            pass
                        print(filenamelistnew, type(filenamelistnew))
                        url_list=[]
                        fileindexlist = []
                        fileindex = 1
                        for url_name in filenamelistnew:
                            fileindexlist.append(str(fileindex))
                            filePath = "http://218.94.64.98:60097" + "/" + name + "/" + url_name     #去掉文件名前的空格
                            url_list.append(filePath)
                            fileindex += 1
                        fileinfolist = zip(filenamelistnew, url_list, fileindexlist)
                        userrole = q.user_role
                        return render(request, 'FinaceNote/Edituserinfo.html', {'userinfo': {'name': request.session['username'], 'editusername': EditUserName,'nickname':nickname,'sex': sex, 'hobby': hobby, 'city':city, 'fileinfolist':fileinfolist, 'userrole':userrole}})
                except:
                    info = '请勾选需要编辑的用户'            # 未勾选用户名点编辑后的报错提醒
                    m = request.session['username']
                    try:
                        userdic = up.objects.exclude(user_name = m).exclude(user_name = "admin")
                        userlist = []
                        rolelist = []
                        for i in userdic:
                            userlist.append(i)
                        print(userlist)
                        for k in userlist:
                            q = up.objects.get(user_name = k)
                            role = q.user_role
                            rolelist.append(role)
                        print(rolelist)
                        userroleinfolist=zip(userlist,rolelist)
                    except:
                        pass
                    return render(request, 'FinaceNote/Manage.html', {'userinfo': {'info': info, 'name':m, 'userroleinfolist': userroleinfolist}})
                try:
                    if action == "删除":
                        q = up.objects.get(user_name = EditUserName)
                        dirpath = "/opt/djangoproject/IronManProject/FinaceNote/upload/{}".format(EditUserName)
                        filenamelist = q.user_filename.replace('[', '').replace(']', '').replace("'","")            #从数据库获取文件名字段类型为‘str’，做字符串过滤掉“[”，“]”，“'”不需要的字符
                        filenamelistnew = filenamelist.split(',')                                                    #根据过滤后的字符串 filenamelist生成文件名列表filenamelistnew
                        print(filenamelistnew, type(filenamelistnew))
                        try:
                            for f in filenamelistnew:
                                fileName = f.replace(' ','')               #根据文件名列表filenamelistnew中的文件名元素，去除空格字符生成实际的文件名
                                print(fileName)                                                              
                                file_path = os.path.join(dirpath, fileName)
                                print(file_path)
                                os.remove(file_path)
                        except:
                            pass
                        os.rmdir(dirpath)
                        q.delete()
                        return redirect('/Manageuserinfo')
                except:
                    info = '请勾选需要删除的用户'            # 未勾选用户名点编辑后的报错提醒
                    m = request.session['username']
                    try:
                        userdic = up.objects.exclude(user_name = m).exclude(user_name = "admin")
                        userlist = []
                        rolelist = []
                        for i in userdic:
                            userlist.append(i)
                        print(userlist)
                        for k in userlist:
                            q = up.objects.get(user_name = k)
                            role = q.user_role
                            rolelist.append(role)
                        print(rolelist)
                        userroleinfolist=zip(userlist,rolelist)
                    except:
                        pass
                    return render(request, 'FinaceNote/Manage.html', {'userinfo': {'info': info, 'name':m, 'userroleinfolist': userroleinfolist}})
            except:
                pass

def ModRole(request):
    if request.session.get('is_login',None):
        if request.method == "POST":
            try:
                Moduser = request.session['EditUserName']
                print(Moduser)
                q = up.objects.get(user_name = Moduser)
                Modrole = request.POST.get('role')
                if Modrole is not None:    
                    q.user_role = Modrole
                    q.save()
                else:
                    pass
                ModNewPass = request.POST.get('newpass') 
                if ModNewPass != '':
                    NewUserPass = make_password(ModNewPass, None, 'pbkdf2_sha256')
                    q.user_password = NewUserPass
                    q.save()
                    info = Moduser + '密码已更改!'
                else:
                    info = Moduser + '密码未更改!'    
                    pass
                if Modrole is None and ModNewPass == '':
                    info = Moduser + '信息未更改!'    
                name = q.user_name
                nickname = q.user_nickname
                sex = q.user_sex
                hobby = q.user_hobby
                city = q.user_city
                userrole = q.user_role
                filenamelist = q.user_filename.replace('[', '').replace(']', '').replace("'","")            #从数据库获取文件名字段类型为‘str’，做字符串过滤掉“[”，“]”，“'”不需要的字符
                filenamelistnew = filenamelist.split(',')                                                    #根据过滤后的字符串 filenamelist生成文件名列表filenamelistnew
                try:                                                                                         # 如果之前上传过带空格文件名的文件filenamelistnew列表中会带出''元素所以需要删除从数据库获取的空字符串，转换成列表的''元素
                    filenamelistnew.remove('')
                except:
                    pass
                print(filenamelistnew, type(filenamelistnew))
                url_list=[]
                fileindexlist = []
                fileindex = 1
                for url_name in filenamelistnew:
                    fileindexlist.append(str(fileindex))
                    filePath = "http://218.94.64.98:60097" + "/" + name + "/" + url_name.replace(' ','')     #去掉文件名前的空格
                    print(filePath)
                    url_list.append(filePath)
                    fileindex += 1
                fileinfolist = zip(filenamelistnew, url_list, fileindexlist)
                return render(request, 'FinaceNote/Edituserinfo.html', {'userinfo': {'info': info, 'name': request.session['username'], 'editusername': name,'nickname':nickname,'sex': sex, 'hobby': hobby, 'city':city, 'fileinfolist':fileinfolist, 'userrole':userrole}})
            except:
                pass






