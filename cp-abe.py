
# coding: utf-8

# In[38]:


import math
import random
import hashlib


# In[25]:


numAttributes = 3

RHO = 8

MAX_BITS = 8


# In[26]:


#Function to check if a number is prime
def isPrime(n):
    if n == 2:
        return True
    
    if n%2 == 0:
        return False
    
    for i in range(3, math.ceil(math.sqrt(n))+1, 2):
        if n%i == 0:
            return False
        
    return True    


# In[27]:


#Function to generate a random prime number of rho bits
def generatePrime(len=MAX_BITS):
    
    temp = random.getrandbits(len)
    
    if len != MAX_BITS:
        temp = temp | (1<<(len-1)) 
    temp |= 1
    
    while not isPrime(temp):
        temp = random.getrandbits(len)
        if len != MAX_BITS: 
            temp = temp | (1<<(len-1)) 
        temp |= 1
    
    return temp


# In[28]:


#Function to find gcd of 'a' and 'b' by Euclid's algorithm
def euclidGcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = euclidGcd(b % a, a)
        return (g, x - (b // a) * y, y)


# In[29]:


#Function to find multiplicative inverse of 'a' modulo 'm'
def moduloInverse(a, m):
    g, x, y = euclidGcd(a, m)
    if g != 1:
        raise Exception('modulo inverse does not exist')
    else:
        return x % m


# In[30]:


#Function to check if 'k' is coprime with all elements of array 'arr' 
def checkCoprimality(k, arr):
    for i in range(len(arr)):
        if math.gcd(k, arr[i]) != 1:
            return False
    return True  


# In[31]:


#Function to calaculate 'a' power 'b' modulo 'n'
def powerModN(a, b, n):
    if b == 0:
        return 1
    
    temp = powerModN(a, b//2, n)
    temp = (temp*temp) % n
    if b%2:
        temp = (temp*a) %n
        
    return temp    


# In[ ]:


#Function to compute one-way hash of given message 'M', with output of length 'len'
def onewayhash(message, len):
    hash_object = hashlib.sha1(b'Hello World')
    hex_dig = hash_object.digest()


# In[32]:


p = generatePrime(RHO)
q = generatePrime(RHO)

while p == q:
    q = generatePrime(RHO)
    
N = p*q

phiN = (p-1)*(q-1)


# In[33]:


pi = [None] * numAttributes
qi = [None] * numAttributes

for i in range(0, numAttributes):
    temp = generatePrime()
    
    while math.gcd(temp, phiN) != 1:
        temp = generatePrime()

    pi[i] = temp  
    qi[i] = moduloInverse(pi[i], phiN)


# In[34]:


k = random.getrandbits(MAX_BITS)

while math.gcd(k, phiN) != 1 and checkCoprimality(k, qi) == False:
    k = random.getrandbits(MAX_BITS)
    
x = random.getrandbits(MAX_BITS)

while checkCoprimality(x, qi) == False:
    x = random.getrandbits(MAX_BITS)    


# In[35]:


g = random.randint(3, N-2)
    
while math.gcd(temp, N) != 1:
    temp = random.randint(3, N-2)


# In[36]:


dU = 1
for i in range(len(qi)):
    dU *= qi[i]

DU = powerModN(g, dU, N)
Y  = powerModN(g,  x, N)
R  = powerModN(g,  k, N)

