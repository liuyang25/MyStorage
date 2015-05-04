#!/usr/bin/python
#coding=utf-8

#string = "Items[#]{item(Item)}"
import google.protobuf
import os
from string import maketrans 
import re
import sys
import struct

#print(sys.stdin.encoding)
#print(sys.stdout.encoding)

"""
fp = open("data.txt")

data = fp.read()

a_v = ord('a')
z_v = ord('z')
A_v = ord('A')
Z_v = ord('Z')

out = []
pat = re.compile(r'[a-z][A-Z]{3}[a-z][A-Z]{3}[a-z]')  
rst = re.findall(pat,data)  
a = []  
for i in rst:  
    print i
    a.append(i[4])  
print(''.join(a)) 
"""

#intab = "abcdefghijklmnopqrstuvwxyz"
#outtab = "cdefghijklmnopqrstuvwxyzab"
#trantab = maketrans(intab, outtab)

#an = re.match('[A-Z][A-Z][A-Z][a-z][A-Z][A-Z][A-Z]', data)
"""
string = "Rewards[,]{items(Items),exp(int),point(int)}"

v = string.split("[")
print v

index = string.find('-')
print index

print string[0:index]



i1 = string.find('[')
i2 = string.find(']')
i3 = string.find('{')
i4 = string.find('}')

if i2 != i1+2 or i3 != i2+1 or i4 < i3+4 :
	print False
else:
	print True
iovdlspnvczsyag
name = string[:i1]
print name
print string[i1+1:i2]
fields = string[i3+1:i4].split(",")
print fields
for field in fields:
	print field


a = {1: "abc"}
print a.values()[0]
print 1 + 2 + 3 + 4
str_ = ""
str_ = "1"
i = float(str_)
print int(i)
"""

"""class Book(object):
    def __setattr__(self, name, value):
        if name == 'value':
            object.__setattr__(self, name, value - 100)
        else:
            object.__setattr__(self, name, value)
    def __getattr__(self, name):
        try:
            return object.__getattribute__(name)
        except:
            return name + ' is not found!'
    def __str__(self):
        return self.name + ' cost : ' + str(self.value)

c = Book()
c.name = 'Python'
c.value = 100
print c.name
print c.value
print c
print c.Type
"""


"""name="hehe"
row=2
col=3
print "stringuct parse failed at sheet:%s row:%s, col:%s" % (name , row, col)
#print "stringuct parse failed at sheet:% row:% col:%" %name%row%col
"""
#print 600016 % 65535

"""
[
     [1],
    [1,1],
   [1,2,1],
  [1,3,3,1],
 [1,4,6,4,1]
]
"""
class Triangle:
    # @return a list of lists of integers
    lists = []
    l = []

    def generate(self, numRows):
        if numRows <= 0 :
            res = self.lists
            self.lists = []
            self.l = []
            return res
        r = [1]
        self.l.append(0)
        for i in range(0, len(self.l)-1):
            r.append(self.l[i] + self.l[i+1])

        self.lists.append(r)
        self.l.pop()
        self.l = r
        return self.generate(numRows-1)
#print "***"
#h = Triangle()
#print h.generate(2)

class Triangle2:
    # @param rowIndex, an integer
    # @return an integer[]
    def __init__(self):
        self.l = []
    def getRow(self, rowIndex):
        if rowIndex < 0 :
            res = self.l
            self.l = []
            return res
        r = [1]
        self.l.append(0)
        for i in range(0, len(self.l)-1):
            r.append(self.l[i] + self.l[i+1])

        self.l.pop()
        self.l = r
        return self.getRow(rowIndex-1)    

h2 = Triangle2()
#print h2.getRow(2)

class UniquePath:
    def __init__(self):
        self.res = {(1,1):1}

    def uniquePaths(self, m, n):
        if self.res.has_key((m,n)):
            return self.res[(m,n)]

        if m < 1 or n < 1:
            return 0

        r1 = self.uniquePaths(m-1,n)
        r2 = self.uniquePaths(m,n-1)
        self.res[(m,n)] = r1 + r2
        return r1 + r2


class UniquePath2:
    # @param obstacleGrid, a list of lists of integers
    # @return an integer
    def __init__(self):
        self.res = {}
    def uniquePaths(self, m, n, ob):
        if self.res.has_key((m,n)):
            return self.res[(m,n)]

        if m < 0 or n < 0:
            return 0

        if ob[m][n] == 1:
            self.res[(m,n)] = 0
            return 0

        r1 = self.uniquePaths(m-1,n, ob)
        r2 = self.uniquePaths(m,n-1, ob)
        self.res[(m,n)] = r1 + r2
        return r1 + r2


    def uniquePathsWithObstacles(self, obstacleGrid):
        ob = obstacleGrid
        m = len(obstacleGrid)
        n = len(obstacleGrid[0])
        if ob[0][0] == 1:
            return 0
        self.res[(0,0)] = 1
        return self.uniquePaths(m-1, n-1, ob)

#b = UniquePath2()
#print b.uniquePathsWithObstacles([[0,0,0],[0,1,0],[0,0,0]])

class EditDistance:
    # @param word1, a string
    # @param word2, a string
    # @return an integer

    def minDistance(self, word1, word2):
        m,n = len(word1), len(word2)
        if m == 0 : return n
        if n == 0 : return m
        edit = [j for j in range(n+1)]
        for i in range(1, m+1):
            left_top, edit[0] = edit[0], i
            for j in range(1, n+1):
                left_top, edit[j] = edit[j], min( edit[j] + 1, edit[j - 1] + 1, left_top + (0 if word1[i-1] == word2[j-1] else 1))
        return edit[n]

e = EditDistance()
print e.minDistance("mart", "karma")

#edit = [j for j in range(5)]
#print edit[1]
#print edit[3]

"""
Given an array S of n integers, are there elements a, b, c, and d in S such that a + b + c + d = target? Find all unique quadruplets in the array which gives the sum of target.

Note:
Elements in a quadruplet (a,b,c,d) must be in non-descending order. (ie, a ≤ b ≤ c ≤ d)
The solution set must not contain duplicate quadruplets.
    For example, given array S = {1 0 -1 0 -2 2}, and target = 0.

    A solution set is:
    (-1,  0, 0, 1)
    (-2, -1, 1, 2)
    (-2,  0, 0, 2)
"""
class FourSum:
    # @return a list of lists of length 4, [[val1,val2,val3,val4]]
    def fourSum(self, num, target):
        if len(num) < 4:
            return []
        num.sort()
        l = len(num)
        if num[0] + num[1] + num[2] + num[3] > target or num[l-1] + num[l-2] + num[l-3] + num[l-4] < target:
            return []

        result = []
        for i1 in range(0, len(num) - 3):
            if i1 > 0 and num[i1] == num[i1-1]:
                continue
            if num[i1] > target/4:
                break
            target2 = target - num[i1]
            for i2 in range(i1 + 1, len(num) - 2):
                if num[i2] == num[i2-1] and i2 > i1 + 1:
                    continue
                if num[i2] > target2/3:
                    break
                target3 = target2 - num[i2]
                if num[l-1] + num[l-2] < target3:
                    continue
                i3 = i2 + 1
                i4 = l - 1
                while i3 < i4:
                    if num[i3] + num[i4] == target3:
                        result.append([num[i1],num[i2], num[i3], num[i4]])
                        i3 += 1
                        while i3 < i4 and num[i3] == num[i3-1]:
                            i3 += 1
                    elif num[i3] + num[i4] > target3:
                        if num[i3] > target3/2:
                            break
                        i4 -= 1
                    else:
                        i3 += 1

        return result

#fs = FourSum()
#print fs.fourSum([-498,-492,-473,-455,-441,-412,-390,-378,-365,-359,-358,-326,-311,-305,-277,-265,-264,-256,-254,-240,-237,-234,-222,-211,-203,-201,-187,-172,-164,-134,-131,-91,-84,-55,-54,-52,-50,-27,-23,-4,0,4,20,39,45,53,53,55,60,82,88,89,89,98,101,111,134,136,209,214,220,221,224,254,281,288,289,301,304,308,318,321,342,348,354,360,383,388,410,423,442,455,457,471,488,488], -2808)

"""
Given a non-negative number represented as an array of digits, plus one to the number.

The digits are stored such that the most significant digit is at the head of the list.
"""
class PlusOne:
    # @param {integer[]} digits
    # @return {integer[]}
    def plusOne(self, digits):
        l = len(digits) - 1
        while l >= 0:
            if digits[l] < 9:
                digits[l] += 1
                return digits
            else:
                digits[l] = 0
                s -= 1
        digits.insert(0, 1)
        return digits

#po = PlusOne()
#print po.plusOne([9,8,7,6,5,4,3,2,1,0])        

class HappyNum:
    # @param {integer} n
    # @return {boolean}
    def __init__(self):
        self._known_num = {}

    def isHappy(self, n):
        if self._known_num.has_key(n):
            if self._known_num[n] == 1:
                return True
            else:
                return False

        self._known_num[n] = 0
        next = 0
        while n != 0:
            next += (n % 10) * (n % 10)
            n = n / 10
        if next == 1:
            self._known_num[n] = 1
            return True
        ret = self.isHappy(next)
        if ret == True:
            self._known_num[n] = 1
        else:
            self._known_num[n] = -1
        return ret


#hn = HappyNum()
#print hn.isHappy(19)
        