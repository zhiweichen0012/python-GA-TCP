# -*- encoding: utf-8 -*-

import random
import math
from GA import GA

class TSP(object):
      def __init__(self, aLifeCount = 100,):
            self.initCitys()
            self.lifeCount = aLifeCount
            self.ga = GA(aCrossRate = 0.7, 
                  aMutationRage = 0.02, 
                  aLifeCount = self.lifeCount, 
                  aGeneLenght = len(self.citys), 
                  aMatchFun = self.matchFun())


      def initCitys(self):
        self.citys = []
        # 这个文件里是34个城市的经纬度
        f = open("./data/distanceMatrix.txt", "r")
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


      def run(self, n = 0):
            while n > 0:
                  self.ga.next()
                  distance = self.distance(self.ga.best.gene)
                  print (("%d : %f") % (self.ga.generation, distance))
                  n -= 1


def main():
      tsp = TSP()
      tsp.run(100)


if __name__ == '__main__':
      main()


