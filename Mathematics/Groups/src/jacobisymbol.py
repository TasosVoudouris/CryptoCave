def jacobi_symbol(a, n):
    if a ==0:
        return 0
    if a ==1:
        return 1
    #write a = 2^e *s where a1 is odd
    e =0
    a1 = a
    while a1 & 1==0: #while a1 is even
        a1>>=1
        e+=1
        
    #if e is even set s = 1
    if e & 1 == 0:
        s = 1
    elif n % 8 == 7 or n % 8 == 1:
        s = 1
    elif n % 8 == 3 or n % 8 == 5:
        s = -1
    
    if n % 4 == 3 and a1 % 4 == 3:
        s = -s
        
    n1 = n % a1
    if a1 ==1:
        return s
    else:
        return s * jacobi_symbol(n1, a1)

print(jacobi_symbol(158, 235))
