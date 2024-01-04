"""
1053：练4.7  求第几项

【题目描述】
对于正整数n,m，求s=1+2+3……+n，当加到第几项时，s的值会超过m？

【输入】
输入m。

【输出】
输出n。

【输入样例】
1000
【输出样例】
45
"""
m = int(input())

sumN = 0
n = 1

while True:
    sumN += n
    if sumN > m:
        break
    n += 1  # n = n + 1

print(n)
