import random
class NormTag:
    def __init__(self,path):
        self.path=path
        self.user_item_all=self.load_data()
        self.train,self.test=self.split_data(0.2)
        self.user_tag,self.user_item,self.tag_item,self.tag_user=self.initsta()
        self.testrecommend()

    def load_data(self):
        user_item_all={}
        i=0
        for line in open(self.path,'r').readlines():
            i=i+1
            user,item,tag,_=line.strip().split('\t')
            user_item_all.setdefault(user,{})
            user_item_all[user].setdefault(item,[])
            user_item_all[user][item].append(tag)
        print('数据条数为{}'.format(i))
        print('用户数为{}'.format(len(user_item_all)))
        return user_item_all

    def split_data(self,ratio,seed=100):
        random.seed(seed)
        train={}
        test={}
        for u in self.user_item_all.keys():
            for i in self.user_item_all[u].keys():
                if random.random()<ratio:
                    test.setdefault(u,{})
                    test[u].setdefault(i,[])
                    for t in self.user_item_all[u][i]:
                        test[u][i].append(t)
                else:
                    train.setdefault(u, {})
                    train[u].setdefault(i, [])
                    for t in self.user_item_all[u][i]:
                        train[u][i].append(t)
        print("训练集样本数 %d, 测试集样本数 %d" % (len(train), len(test)))
        return train,test

    def initsta(self):
        user_tag={}
        user_item={}
        tag_item={}
        tag_user={}
        for u,items in self.train.items():
            for i,tags in items.items():
                for t in tags:
                    self.addValueToMat(user_tag,u,t)
                    self.addValueToMat(user_item,u,i)
                    self.addValueToMat(tag_item,t,i)
                    self.addValueToMat(tag_user,t,u)
        print("user_tags大小 %d, tag_items大小 %d, user_items大小 %d" % (len(user_tag), len(tag_item), len(user_item)))
        return user_tag, user_item, tag_item,tag_user

    def addValueToMat(self,m,p,q):
        if p not in m:
            m.setdefault(p,{})
            m[p].setdefault(q,1)
        else:
            if q not in m[p]:
                m[p][q]=1
            else:
                m[p][q]=m[p][q]+1



    def recommend(self,user,N):
        recommend_items={}
        item=self.user_item[user]
        for t,v in self.user_tag[user].items():
            for i,n in self.tag_item[t].items():
                if i in item:
                    continue
                if i not in recommend_items:
                    recommend_items[i] = v * n / (len(self.user_tag[user]) * len(self.tag_user[t]))
                    #recommend_items[i] = v * n
                else:
                    recommend_items[i]=recommend_items[i]+v*n/(len(self.user_tag[user]) * len(self.tag_user[t]))
                    #recommend_items[i] = recommend_items[i]+v*n
        return sorted(recommend_items.items(), key=lambda x:x[1], reverse=True)[0:N]

    def preandrecall(self,N):
        r=0
        p=0
        q=0
        for user,item in self.test.items():
            if user not in self.train:
                continue
            rank=self.recommend(user,N)
            for t,score in rank:
                if t in item:
                    r=r+1
            p=p+N
            q=q+len(item)
        return (r/q, r/p)

    def testrecommend(self):
        print("推荐结果评估")
        print("%3s %10s %10s" % ('N', "精确率", '召回率'))
        for n in [5,10,20,40,60,80,100]:
            rec,pre=self.preandrecall(n)
            print("%3d %10.3f%% %10.3f%%" % (n, pre * 100, rec * 100))


if __name__=='__main__':
    nt=NormTag('user_taggedbookmarks-timestamps.dat')















