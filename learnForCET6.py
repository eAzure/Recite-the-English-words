import os
import operator
import random
#实现单词结构体
class wordClass(object):
    class Struct(object):
        def __init__(self,word,chMeaning,falseTime,viewTime,perFalseTime):
            self.word=word  #英语单词
            self.chMeaning=chMeaning    #汉语意思
            self.falseTime=falseTime  #错误次数
            self.viewTime=viewTime   #浏览次数
            self.perFalseTime=perFalseTime  #本次错误数
    def make_struct(self,word,chMeaning,falseTime,viewTime,perFalseTime):
        return self.Struct(word,chMeaning,falseTime,viewTime,perFalseTime)

wordList=[]#存放读入的单词列表，里面存的是wordClass类型
selectedWordList=[]#本次被选中的单词


falseWordList=[]#存放学习过程中错误的单词

word=wordClass()#声明该类对象

#单词的预处理（读进）
def wordPreProcess(filePath,lineNum):
    # 读取文件"C:/Users/LGX/Desktop/CET6.txt"
    f = open(filePath)
    line = f.readline()
    while line:

        lineNum += 1
        # 对读入的单词表进行处理
        # print(len(line.split()))
        # 读入单词
        if len(line.split()) == 2:
            wordList.append(word.make_struct(line.split()[0], line.split()[1], 0, 0,0))
        else:
            wordList.append(word.make_struct(line.split()[0], line.split()[1], line.split()[2], line.split()[3],line.split()[4]))

        line = f.readline()
    f.close()
    return lineNum

#单词排序方法(优先按错误数排序（按错误数从大到小），再按浏览数(从小到大))
#根据你选择的学习单词数生成本次学习的单词
def generateLearnWord(wordNum,lineNum):
    wordList.sort(key=operator.attrgetter('falseTime','viewTime'),reverse=True)
    #根据单词数和所要学习的单词数进行本次单词的选择
    #采取的策略为所选单词数按3：1分配在总单词数里的1：3，按随机策略进行分配
    lineNum1=int(lineNum/3)
    wordNum1=int(wordNum/3)
    wordNum2=wordNum-wordNum1
    randNumList1=random.sample(range(0,lineNum1),wordNum2)#生成互不相同的在重要单词的前半部分的单词的序号
    randNumList2=random.sample(range(lineNum1,lineNum),wordNum1)#生成在互不相同的在后面部分的单词的序号
    #将选中的单词加入到应学习单词的列表里
    for i in randNumList1:
        selectedWordList.append(wordList[i])
    for i in randNumList2:
        selectedWordList.append(wordList[i])

#单词学习的过程
def learnProcess():
    print('现在开始学习:')
    for i in selectedWordList:
        print(i.word+'   中文含义为：   '+i.chMeaning)
        #在这里需改正该单词的viewTime的数量，即改正wordList里面的
        index=wordList.index(i)#获取对应下标
        wordList[index].viewTime=int(wordList[index].viewTime)
        wordList[index].viewTime+=1

        #由于python3目前无官方监听键盘的库，好像有个pyHook非官方可用
        #我们在这里的就按下一个来进行吧
        ansInput=input("是否继续？（y）")
        if ansInput=='y':
            continue
    print("恭喜你全部学完！下面开始检查学习效果：")
    #在这里采用一种方法来进行打乱顺序
    random.shuffle(selectedWordList)#妙啊！
    print("请根据屏幕上的中文含义输入英文单词：")
    for i in selectedWordList:
        print(i.chMeaning)
        inputWord=input("请输入正确的英文单词：")
        if inputWord==i.word:
            print("答对了！看下一个：")
            continue
        else:
            print("很遗憾！正确的英文单词为："+i.word)
            #下面进行答错单词的处理
            #1、将其加入到本次的错误单词列表里
            #2、并改正其falseTime的数量
            falseWordList.append(i)
            index=wordList.index(i)
            wordList[index].falseTime=int(wordList[index].falseTime)
            wordList[index].falseTime+=1
            wordList[index].perFalseTime=int(wordList[index].perFalseTime)
            wordList[index].perFalseTime+=1
            continue
    if len(falseWordList):
        print('---------------------------------')
        print('下面进行本次错误单词的学习：')
        print('规则如下：每答错一个单词，该单词的本次错误数加1，答对则本次错误数减1，减到0为止')

    while(len(falseWordList)):
        for i in falseWordList:
            print(i.chMeaning)
            inputWord = input("请输入正确的英文单词：")
            if inputWord == i.word:
                print('答对了！')
                index=falseWordList.index(i)
                falseWordList[index].perFalseTime-=1
                if falseWordList[index].perFalseTime==0:
                    falseWordList.remove(i)
            else:
                index = falseWordList.index(i)
                print('很遗憾！正确的英文单词为：'+falseWordList[index].word)
                falseWordList[index].perFalseTime += 1

    print("恭喜你全部学习完毕！")


#学习完后对文件的处理
def afterLearning(filePath):
    #将更改后的单词和浏览次数写回文件里
    with open(filePath,'w') as file_obj:
        for i in wordList:
            lineWrite=str(i.word)+' '+str(i.chMeaning)+' '+str(i.falseTime)+' '+str(i.viewTime)+' '+str(i.perFalseTime)+'\n'
            file_obj.write(lineWrite)




if __name__ == '__main__':
    print('---------------------------------------')
    print('欢迎使用CET6单词背诵程序！')
    print('---------------------------------------')
    filePath = input('请输入你所要背的单词文件地址：')
    wordNum = input('请输入你要背诵的单词的个数：')

    wordNum=int(wordNum)

    lineNum = 0  # 单词本行数
    #读入单词
    lineNum=wordPreProcess(filePath,lineNum)

    #根据你要背诵的单词的个数生成本次需要学习的单词
    generateLearnWord(wordNum,lineNum)

    #选中完单词后便可进行学习
    learnProcess()

    #学习完后的处理
    afterLearning('C:/Users/LGX/Desktop/CET6Test.txt')

