from gmpy2 import *
from random import randint
import math
import sys
__author__ = 'Bob wang'

class Pollard_rho:

    def __init__(self, input):
        self.N = input
        self.factors = []

    def f(self, x, a, b):
        return a*x*x + b

    def findFactor(self, n):
        maxiterssq = 0.7854*n
        x = randint(1, n-1)
        y = x
        d = 1
        iters = 0
        a = randint(1, n-1)
        b = randint(1, n-1)
        while d == 1 or d == n:
            if iters*iters > maxiterssq:
                a = randint(1, n-1)
                b = randint(1, n-1)
                x = randint(1, n-1)
                y = x
                iters = 0
            x = self.f(x, a, b) % n
            y = self.f(self.f(y, a, b), a, b) % n
            d = gcd(abs(x-y), n)
            iters += 1
        return d

    def findPrimeFactor(self, n, factors):
        if is_prime(n):
            factors.append(n)
        else:
            temp = n // self.findFactor(n)
            self.findPrimeFactor(temp, factors)

    def factor(self):
        while self.N % 2 == 0:
            self.factors.append(2)
            self.N //= 2
        while self.N % 3 == 0:
            self.factors.append(3)
            self.N //= 3
        while self.N > 1:
            self.findPrimeFactor(self.N, self.factors)
            self.N //= self.factors[-1]
        self.factors.sort()
        self.factors = list(set(self.factors))

class FuckCGL:
    def __init__(self, input):
        self.N = input
        self.prlist = []

    def Phi(self, N):
        if(N < 1):
            return 0
        if(N == 1):
            return 1
        if(is_prime(N)):
            return N-1
        fac = Pollard_rho(N)
        fac.factor()
        pfs = fac.factors
        prod = N
        for pfi in pfs:
            prod = prod*(pfi-1)/pfi
        return prod


    def generate_all(self, g, N):
        phi = self.Phi(N)
        prlist = []
        for d in range(phi):
            if (gcd(phi, d) == 1):
                prlist.append(int(pow(g, d, N)))
        prlist.sort()
        return prlist

    def solve_primeN(self, N):
        assert(is_prime(N) and (N%2==1))

        fac = Pollard_rho(N-1)
        fac.factor()
        factors = fac.factors

        for i in range(1, N):
            flag = True
            for j in factors:
                if (pow(i, (N-1)/j, N) == 1):
                    flag = False
                    break
            if (flag == True and pow(i, N-1, N)==1 ):
                break
        prlist = self.generate_all(i, N)
        assert(len(prlist) == self.Phi(self.Phi(N)))
        return prlist

    def solve_squareN(self, N):
        sqrt = iroot(N,2)[0]
        assert(iroot(N,2)[1] and is_prime(sqrt) and (sqrt%2==1))
        ans = self.solve_primeN(sqrt)
        for i in ans:
            assert((pow(i, sqrt-1, N) != 1) or (pow(i+sqrt, sqrt-1, N) != 1))
            if pow(i, sqrt-1, N) != 1:
                pr = i
                break
            if (pow(i+sqrt, sqrt-1, N) != 1):
                pr = int(i+sqrt)
                break
        prlist = self.generate_all(pr, N)
        assert(len(prlist) == self.Phi(self.Phi(N)))
        return prlist

    def solve_evenN(self, N):
        prlist = []
        assert(N % 2 == 0)
        half = N/2
        if (is_prime(half) and (half %2 == 1)):
            tmp = self.solve_primeN(half)
            for pr in tmp:
                assert((pr % 2 == 1) or ((pr+half)%2 ==1) )
                if pr % 2 == 1:
                    prlist.append(pr)
                if ((pr+half)%2 ==1):
                    prlist.append(pr+half)
            prlist.sort()
            assert(len(prlist) == self.Phi(self.Phi(N)))
            return prlist

        p = iroot(half, 2)[0]
        if not iroot(half,2)[1]:
            raise ValueError
        assert(is_prime(p) and p%2==1)
        tmp = self.solve_squareN(p*p)
        for pr in tmp:
            assert((pr % 2 == 1) or ((pr+half)%2 ==1) )
            if pr % 2 == 1:
                prlist.append(pr)
            if ((pr+half)%2 ==1):
                prlist.append(pr+half)
        prlist.sort()
        assert(len(prlist) == self.Phi(self.Phi(N)))
        return prlist

    def solve_all(self):
        if is_prime(self.N):
            self.prlist = self.solve_primeN(self.N)
        elif iroot(self.N,2)[1] and is_prime(iroot(self.N,2)[0]):
            self.prlist = self.solve_squareN(self.N)
        else:
            self.prlist = self.solve_evenN(self.N)


def main():
    N = eval(sys.argv[1])
    solvepr = FuckCGL(N)
    solvepr.solve_all()
    print(solvepr.prlist)

if __name__ == '__main__':
    main()
