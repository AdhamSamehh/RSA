import random



        
def is_prime(n, k=8):
    """
    Miller-Rabin primality test.
    Returns True if n is probably prime, False if it's definitely composite.
    k is the number of tests to perform.
    """
    # Basic checks
    if n <= 1:  # 1 and below are not prime
        return False
    if n <= 3:  # 2 and 3 are prime
        return True
    if n % 2 == 0:  # Even numbers greater than 2 are not prime
        return False

    # Write n as 2^r * d + 1
    r, m = 0, n - 1
    while m % 2 == 0:  # Get r and d such that n - 1 = 2^r * d
        r += 1
        m //= 2

    # Witness loop
    for _ in range(k):  # Repeat the test k times
        a = random.randint(2, n - 2)  # Choose a random base
        x = pow(a, m, n)  # Compute a^d mod n
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)  # Compute x^2 mod n
            if x == n - 1:
                break
        else:
            return False  # Definitely composite if conditions fail

    return True  # Probably prime if all tests passed

def generate_random_prime(bits):
    """
    Generate a random prime number with 'bits' number of bits.
    """
    while True:
        hopefully_prime = random.randint(2**(bits - 1), 2**bits - 1)  # Generate a random num
        if is_prime(hopefully_prime):  # Check if num is prime
            return hopefully_prime  # Return num candidate

def prime_factorization(n):
    i = 2
    factors = {}
    while i * i <= n:
        while (n % i) == 0:
            if i in factors:
                factors[i] += 1
            else:
                factors[i] = 1
            n //= i
        i += 1
    if n > 1:
        factors[n] = 1
    return factors

def gcd(a, b):
    """
    Returns the greatest common divisor of two numbers a and b.
    """
    # Get the prime factorization of both numbers
    factors_of_a = prime_factorization(a)
    factors_of_b = prime_factorization(b)
    
    # Initialize gcd to 1
    gcd_value = 1
    
    # Iterate through common prime factors and multiply them
    for factor in factors_of_a.keys():
        if factor in factors_of_b:
            gcd_value *= factor ** min(factors_of_a [factor], factors_of_b [factor])
    
    return gcd_value

def encrypt(text, public_key):
    # Encrypts any text Using the RSA Encryption Algorithm 
    n, e = public_key
    return pow(text, e, n)

def decrypt(text, private_key):
    # Decrypts any text Using the RSA Decryption Algorithm 
    n, d = private_key
    return pow(text, d, n)

def generate_rsa_keys(bits):
    """
    Generates RSA public and private keys.
    """
    # Generate two random prime numbers
    p = generate_random_prime(bits // 2)
    q = generate_random_prime(bits // 2)
    
    # Compute modulus n and Euler's totient function phi
    n = p * q
    phi = (p - 1) * (q - 1)
    
    # Choose encryption exponent e
    e = random.randint(2, phi - 1)
    while gcd(e, phi) != 1:
        e = random.randint(2, phi - 1)
    
    # Compute decryption exponent d
    d = pow(e, -1, phi)
    
    # Return public and private keys
    public_key = (n, e)
    private_key = (n, d)
    
    return public_key, private_key



# Example usage:
bits = int(input("Please enter 8 or 16: "))  # Adjust the number of bits as needed
public_key, private_key = generate_rsa_keys(bits)  # Generate RSA keys
print("Public key:", public_key)  # Print public key
print("Private key:", private_key)  # Print private key