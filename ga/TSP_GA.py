# encoding: utf-8
'''
@author: zhiwei

@contact: zhiweichen95@126.com
@software: PyCharm
@file: TSP_GA.py.py
@time: 2018/11/13 9:49 AM
'''
import random
import math
from GATCP.GA import GA
# if sys.version_info.major < 3:
#       import Tkinter
# else:
#       import tkinter as Tkinter

# -*- encoding: utf-8 -*-

import math
from GA import GA


class TSP(object):
    def __init__(self, aLifeCount=100, ):
        self.initCitys()
        self.lifeCount = aLifeCount  # 种群数量，就是每次我们在多少个城市序列里筛选，这里初始化为100
        self.ga = GA(aCrossRate=0.6,
                     aMutationRage=0.03,
                     aLifeCount=self.lifeCount,
                     aGeneLenght=len(self.citys),
                     aMatchFun=self.matchFun())

    def initCitys(self):
        self.citys = []
        # 这个文件里是34个城市的经纬度
        f = open("../data/distanceMatrix.txt", "r")
        while True:
            # 一行一行读取
            loci = str(f.readline())
            if loci:
                pass  # do something here
            else:
                break
            # 用readline读取末尾总会有一个回车，用replace函数删除这个回车
            loci = loci.replace("\n", "")
            # 按照tab键分割
            loci = loci.split("\t")
            # 中国34城市经纬度读入citys
            self.citys.append((float(loci[1]), float(loci[2]), loci[0]))

    # order是遍历所有城市的一组序列，如[1,2,3,7,6,5,4,8……]
    # distance就是计算这样走要走多长的路
    def distance(self, order):
        distance = 0.0
        for i in range(-1, len(self.citys) - 1):
            index1, index2 = order[i], order[i + 1]
            city1, city2 = self.citys[index1], self.citys[index2]
            distance += math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

            """
            R = 6371.004
            Pi = math.pi 
            LatA = city1[1]
            LatB = city2[1]
            MLonA = city1[0]
            MLonB = city2[0]

            C = math.sin(LatA*Pi / 180) * math.sin(LatB * Pi / 180) + math.cos(LatA * Pi / 180) * math.cos(LatB * Pi / 180) * math.cos((MLonA - MLonB) * Pi / 180)
            D = R * math.acos(C) * Pi / 100
            distance += D
            """
        return distance

    def matchFun(self):
        return lambda life: 1.0 / self.distance(life.gene)

    def run(self, n=0):
        while n > 0:
            self.ga.next()
            distance = self.distance(self.ga.best.gene)
            print (("%d : %f") % (self.ga.generation, distance))
            n -= 1
        print "经过%d次迭代，最优解距离为：%f" % (self.ga.generation, distance - 1)
        print "遍历城市顺序为："
        # print "遍历城市顺序为：", self.ga.best.gene
        # 打印出我们挑选出的这个序列中
        for i in self.ga.best.gene:
            print self.citys[i][2]


def main():
    tsp = TSP()
    tsp.run(500)


if __name__ == '__main__':
    main()
