def longest_substring(s):
    start = 0
    end = 0
    max_len = 0
    
    while end < len(s):
        # 如果end指向的字符大于等于start指向的字符,更新max_len
        if s[end] >= s[start]:
            max_len = max(max_len, end - start + 1)
            end += 1
        # 否则,移动start指针    
        else:
            start += 1
            
    return max_len

print(longest_substring('sishfbbegha')) # 6
print(longest_substring('aaaa')) # 4
print(longest_substring('cbaedf')) # 3