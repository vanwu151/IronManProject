# a = []
# print(len(a))

# q = up(user_name = v1, user_sex = v2, user_hobby = v3, user_city = v4, user_pass = v5)

# conn = MySQLdb.connect(
#     host='172.18.10.152',
#     port=3306,
#     user='root',
#     passwd=django_pass.mysqlpass,
#     db='finacenote',
# )
# q.save()
# cur = conn.cursor()
# cur.execute("insert into finacenote_upload (user_name, user_sex, user_hobby, user_city, user_pass)values('{}','{}','{}','{}','{}');".format(v1, v2, v3, v4, v5))
# cur.close()
# conn.commit()
# conn.close()

# def paixu(l):
#     l2 = []
#     l2 = l[0:2]
#     if l2[0] < l2[1]:
#         m = l.pop(0)
#     else:
#         m = l.pop(1)
#     return l
# def sort(l):
#     for i in range(len(l) - 1):
#         # print('i:{}'.format(i))
#         for j in range((len(l)) - 1 - i):
#             # print('j:{}'.format(j))
#             if l[j] > l[j+1]:
#                 l[j],l[j+1] = l[j+1],l[j]
#                 # print('l[j]:{} l[j+1]:{}'.format(l[j],l[j+1]))
#     return l

# def fib(l):
#     for i in range(0, len(l)-1):
#         for j in range(0, len(l) - 1 -i):
#             if l[j] < l[j+1]:
#                 l[j], l[j+1] = l[j], l[j+1]
#     return l


# if __name__ == "__main__":

# b = a.replace('[', '').replace(']', '')
# print(b)
# l = b.split(',')
# print(l, len(l))
# print(sort(l))
# print(fib(l))

# import nacos

# print(dir(nacos))

# SERVER_ADDRESSES = "172.18.99.19:8848"
# NAMESPACE = "ba0348be-923d-4393-862c-af500ea09ad4"

# client = nacos.NacosClient(SERVER_ADDRESSES, namespace=NAMESPACE)

# # get config
# data_id = "id"
# group = "DEFAULT_GROUP"
# print(client.get_config(data_id, group))
import re        
a = [11,234,543,12,124,3234,12,3234,123,122,54,43,235,556,42,1243,212,12,145,643,234,'sql server迁移一张表.docx']
b = [116,234,543,12,124,3234,12,3234,123,122,54,43,235,556,42,1243,212,12,145,643,234,'sql server迁移一张表.docx']
c = zip(a,b)
for j,i in c:
    print(j, i)
# if 11 in a:
#     print('yes')
print(a.index('sql server迁移一张表.docx') + 1)    

# pattern = re.compile(r' +')
# for i in a:
#     print(i)
#     m = pattern.findall(str(i))
#     if m:
#         for y in m:
#             print(y)
#             print('yes')
#     else:
#         print('no')
