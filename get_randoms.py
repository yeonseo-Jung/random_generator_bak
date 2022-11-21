import math
import random

def get_1_or_0() -> int:
    return int(round(random.random(), 0))

def get_random_element(_list: list) -> int or str:
    # get_1_or_0()을 활용한 리스트 원소 랜덤 추출 함수
    
    if len(_list) == 1:
        return _list[0]
    
    elif len(_list) == 0:
        raise ValueError("빈 리스트 혹은 원소 개수가 한개입니다.")
    
    else:
        _list_: list = []
        while len(_list_) != 1:
            for elm in _list:
                if get_1_or_0() == 1:
                    _list_.append(elm)
                    
            if len(_list_) > 1:
                _list = _list_
                _list_ = []
        
        return _list_[0]

def get_increment(m: int) -> tuple:
    """
    c(increment)값 결정
        - c와 m은 서로소 (0<= c < m)
    """
    
    flag: bool = False
    coprime: int = 1
    coprimes: list = []
    for i in range(2, m):
        if math.gcd(m, i) == 1:
            # get random 1 or 0
            if get_1_or_0() == 1:
                coprimes.append(i)
                coprime *= i
        
                # 계수 크기 조정
                while coprime >= m:
                    _coprime = get_random_element(coprimes)
                    coprime //= _coprime
                    flag = True
        if flag:
            break
        
    if not math.gcd(coprime, m) or coprime >= m:
        raise ValueError("서로소를 잘못구했습니다!")
        
    return coprime, coprimes

def get_multiplier(m: int) -> tuple:
    """
    a(multiplier)값 결정
        - m이 4의 배수이면 a-1도 4의 배수
        - a-1은 m의 모든 소인수*로 나누어 떨어짐
        * 연산 시간 문제와 계수 예측을 막기 위해 소인수 전체집합의 부분집합의 곱으로 설정함
        (get_1_or_0 함수를 통해 랜덤하게 구함)
    """
    
    # 점화식 연산 횟수가 10 ** 7 초과 되는것을 방지
    max_len = 8

    m_org = m
    
    # b = a - 1
    # 4의 배수 조건 체크
    if m % 4 == 0:
        b = 4
        m //= 4
    else:
        b = 1

    factor: int = 2
    factors: list = []
    while factor**2 <= m:
        # b값 설정: 소인수 분해
        while m % factor == 0:
            m = m // factor
            # get random 1 or 0
            if get_1_or_0() == 1:
                factors.append(factor)
                b *= factor
                # 계수 크기 조정
                while b >= m_org or len(str(b)) >= max_len:
                    _factor = get_random_element(factors)
                    b //= _factor
            
        factor += 1
        
    if m > 1:
        # get random 1 or 0
        if get_1_or_0() == 1:
            factors.append(m)
            b *= m
            # 계수 크기 조정
            while b >= m_org or len(str(b)) >= max_len:
                _factor = get_random_element(factors)
                b //= _factor    
                
    a = b + 1
    
    return a, factors

def get_random(n: int, interations: int = None) -> tuple:
    """
    Linear congruential generator
        Recurrence Relation: Xn+1 = (a * Xn + c) % m
        c: increment, a: multiplier, m: modulus
        
        ** 주기가 최대가 되기위한 계수 조건 ** 
            - c와 n은 서로소 (0<= c < n) 
            - m이 4의 배수이면 a-1도 4의 배수
            - a-1은 m의 모든 소인수*로 나누어 떨어짐
                * 연산 시간 문제와 계수 예측을 막기 위해 소인수 전체집합의 부분집합의 곱으로 설정함
                  (get_1_or_0 함수를 통해 랜덤하게 구함)
    """
    
    # 폐구간 [0, n] 사이의 임의의 정수 1개 return
    m = n + 1
    seed = get_1_or_0() # seed
    a, factors = get_multiplier(m)
    c, coprimes = get_increment(m)

    x: int = seed
    i: int = 0
    randoms: list = []
    if interations is None:
        while i < a:
            x = (a * x + c) % m
            randoms.append(x)
            i += 1  
    else:
        while i < interations:
            x = (a * x + c) % m
            randoms.append(x)
            i += 1    
        
    return x, randoms, seed, a, factors, c, coprimes