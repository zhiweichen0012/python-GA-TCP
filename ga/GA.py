# encoding: utf-8
'''
@author: zhiwei

@contact: zhiweichen95@126.com
@software: PyCharm
@file: GA.py
@time: 2018/11/13 9:48 AM
'''

import random
from GATCP.Life import Life


class GA(object):
    """遗传算法类"""

    def __init__(self, aCrossRate, aMutationRage, aLifeCount, aGeneLenght, aMatchFun=lambda life: 1):
        self.croessRate = aCrossRate  # 交叉概率
        self.mutationRate = aMutationRage  # 突变概率
        self.lifeCount = aLifeCount  # 种群数量，就是每次我们在多少个城市序列里筛选，这里初始化为100
        self.geneLenght = aGeneLenght  # 其实就是城市数量
        self.matchFun = aMatchFun  # 适配函数
        self.lives = []  # 种群
        self.best = None  # 保存这一代中最好的个体
        self.generation = 1  # 一开始的是第一代
        self.crossCount = 0  # 一开始还没交叉过，所以交叉次数是0
        self.mutationCount = 0  # 一开始还没变异过，所以变异次数是0
        self.bounds = 0.0  # 适配值之和，用于选择是计算概率

        self.initPopulation()  # 初始化种群

    def initPopulation(self):
        """初始化种群"""
        self.lives = []
        # gene = [0,1,…… ,self.geneLength-1]
        # 事实就是0到33
        for i in range(self.lifeCount):
            gene = [x for x in range(self.geneLenght)]
            random.shuffle(gene)
            life = Life(gene)
            self.lives.append(life)

    def judge(self):
        """评估，计算每一个个体的适配值"""
        self.bounds = 0.0  # 适配值之和，用于选择时计算概率 选择函数
        self.best = self.lives[0]  # 假设种群中的第一个基因被选中
        for life in self.lives:
            life.score = self.matchFun(life)
            self.bounds += life.score
            if self.best.score < life.score:  # 如果新基因的适配值大于原先的best基因，就更新best基因
                self.best = life

    def cross(self, parent1, parent2):
        """交叉"""
        # 取parent2里面的index1到index2片段，其他的都取parent1，进行交叉，组成新的基因序列
        index1 = random.randint(0, self.geneLenght - 1)
        index2 = random.randint(index1, self.geneLenght - 1)
        tempGene = parent2.gene[index1:index2]  # 交叉的基因片段
        newGene = []
        p1len = 0
        for g in parent1.gene:
            if p1len == index1:
                newGene.extend(tempGene)  # 插入基因片段
                p1len += 1
            if g not in tempGene:
                newGene.append(g)
                p1len += 1
        self.crossCount += 1
        return newGene

    def mutation(self, gene):
        """突变"""
        # 其实就是在这个基因序列中调换了两个基因位置，下标index1和index2的基因互换位置
        # 相当于取得0到self.geneLength - 1之间的一个数，包括0和self.geneLength - 1
        index1 = random.randint(0, self.geneLenght - 1)
        index2 = random.randint(0, self.geneLenght - 1)

        newGene = gene[:]  # 产生一个新的基因序列，以免变异的时候影响父种群
        newGene[index1], newGene[index2] = newGene[index2], newGene[index1]
        self.mutationCount += 1
        return newGene

    def getOne(self):
        """选择一个个体"""
        r = random.uniform(0, self.bounds)
        for life in self.lives:
            r -= life.score
            if r <= 0:
                return life

        raise Exception("选择错误", self.bounds)

    def newChild(self):
        """产生新的后代"""
        parent1 = self.getOne()
        rate = random.random()
        # 按概率交叉
        if rate < self.croessRate:
            # 交叉
            parent2 = self.getOne()
            gene = self.cross(parent1, parent2)
        else:
            gene = parent1.gene
        # 按概率突变
        rate = random.random()
        if rate < self.mutationRate:
            gene = self.mutation(gene)
        return Life(gene)

    def next(self):
        """产生下一代"""
        self.judge()
        newLives = []
        newLives.append(self.best)  # 把最好的个体加入下一代
        while len(newLives) < self.lifeCount:
            newLives.append(self.newChild())
        self.lives = newLives
        self.generation += 1
