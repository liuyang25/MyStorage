#coding=utf-8

#string = "Items[#]{item(Item)}"
import google.protobuf
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

"""name="hehe"
row=2
col=3
print "stringuct parse failed at sheet:%s row:%s, col:%s" % (name , row, col)
#print "stringuct parse failed at sheet:% row:% col:%" %name%row%col
"""
#print 600016 % 65535