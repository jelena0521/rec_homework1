# 仅为学习日记，不可用于任何商业用途
#基于norm和tfidf分析delicious-2k数据
#1、load_data加载数据，获得第一个字典{用户：{物品：次数}}
#2、分割数据 使用两个for循环
#3、初始化4个细分字典user_tag,user_item,tag_item,tag_user
#4、定义初始化填入的数据
#5、计算norm后的推荐指数，进行倒序  sum（用户对每个tag的关联度*每个tag对item的关联度）
    recommend_items[i]=recommend_items[i]+v*n/(len(self.user_tag[user]) * len(self.tag_user[t]))
    recommend_items[i]：表示对特定用户推荐物品i的概率
    v:用户对此tag的评价次数
    n:此tag被物品i打标签的次数
    len(self.user_tag[user])：用户打了多少个tag
    len(self.tag_user[t])：此tag被多少用户打过
 #6、计算精确率、召回率、f1
 精确率p=推荐为真且实际为真的数量/推荐为真的数量
 号回率r=推荐为真且实际为真的数量/实际为真的数量
 f1=2*p*q/(p+q)
 #如果是tfidf修改第5项
 recommend_items[i]=recommend_items[i]+v*n/math.log(1+len(self.tag_user[t]))
 
