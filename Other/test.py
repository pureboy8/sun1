s = 'sishfbbegha'
ans= ''
ansList=[]
if len(s) <= 1:
    ans = s[:]
    ansList.append(ans)
else:
    ans +=  s[0]
    for i in range(1,len(s)):
        if s[i-1] <= s[i]:
            if s[i] <= s[i+1]:
                ans += s[i]
                ansList+= ans
            else:
                ansList=s[i:]
        else:
            ansList = ans
print (ansList)