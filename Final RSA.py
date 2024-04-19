import random
import math
import time

def generate_rsa_keys(bit_length):
    while True:
        start_time = time.time()
        p = generate_prime_number(bit_length // 2)
        q = generate_prime_number(bit_length // 2)
        n = p * q
        phi_n = (p - 1) * (q - 1)
        
        if phi_n <= 2:
            continue  # Restart the loop to regenerate primes
        
        e = choose_public_exponent(phi_n)
        d = modular_inverse(e, phi_n)
        public_key = (e, n)
        private_key = (d, n)
        end_time = time.time()
        runtime = end_time - start_time
        return public_key, private_key, runtime


def generate_prime_number(bit_length):
    while True:
        candidate = random.getrandbits(bit_length)
        if is_prime(candidate):
            return candidate

def is_prime(n, k=5):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False
    r = 0
    d = n - 1
    while d % 2 == 0:
        d //= 2
        r += 1
    def miller_rabin_test(a):
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            return True
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                return True
        return False
    for _ in range(k):
        a = random.randrange(2, n - 1)
        if not miller_rabin_test(a):
            return False
    return True

def choose_public_exponent(phi_n):
    if phi_n <= 2:
        raise ValueError("phi_n must be greater than 2 to choose a public exponent.")
    e = random.randint(2, phi_n - 1)
    while math.gcd(e, phi_n) != 1:
        e = random.randint(2, phi_n - 1)
    return e



def extended_euclidean_algorithm(a, b):
    if b == 0:
        return a, 1, 0
    gcd, x1, y1 = extended_euclidean_algorithm(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return gcd, x, y

def modular_inverse(e, phi_n):
    gcd, x, _ = extended_euclidean_algorithm(e, phi_n)
    if gcd == 1:
        return x % phi_n
    else:
        raise ValueError("No modular inverse exists")

def factor_modulus(N):
    for i in range(2, int(math.sqrt(N)) + 1):
        if N % i == 0:
            return i, N // i
    raise ValueError("Modulus cannot be factored into prime numbers")

def crack_private_key_brute_force(public_key):
    # Attempts to Crack the Private Key Using a Brute Force Approach 
    n, e = public_key

    start_time = time.time()  # Record Start Time

    p, q = None, None
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            p = i
            q = n // i
            break

    if p is None or q is None:
        print("Failed to find suitable prime factors for modulus.")
        return None, 0

    phi = (p - 1) * (q - 1)
    
    # Calculate the modular inverse of e modulo phi
    d = modular_inverse(e, phi)

    end_time = time.time()  # Record End Time
    runtime = end_time - start_time  # Calculate Runtime

    return (n, d), runtime



def main():
    print("Welcome to RSA Key Generator and Private Key Cracker\n")
    bit_length = 0
    while bit_length not in [8, 16]:
        try:
            bit_length = int(input("Enter the desired bit length for RSA keys (8 or 16): "))
            if bit_length not in [8, 16]:
                raise ValueError
        except ValueError:
            print("Invalid input. Please enter either 8 or 16.")

    method = None
    while method not in ['1', '2']:
        method = input("\nChoose the method to find the private exponent:\n"
                       "1. Factorization\n"
                       "2. Brute force\n"
                       "Enter the corresponding number: ")

    print("\nGenerating RSA keys...")
    public_key, private_key, generation_time = generate_rsa_keys(bit_length)
    print("\nRSA keys generated successfully!")
    print("\nPublic Key (e, n):", public_key)
    print("Private Key (d, n):", private_key)
    print(f"Key generation runtime: {generation_time:.6f} seconds")

    print("\nAttempting to crack the private key...")
    if method == '1':
        try:
            p, q = factor_modulus(public_key[1])
            start_time = time.time()
            d_factorized = modular_inverse(public_key[0], (p - 1) * (q - 1))
            end_time = time.time()
            factorization_time = end_time - start_time
            print("Private exponent (d) cracked using factorization method:", d_factorized)
            print(f"Factorization runtime: {factorization_time:.6f} seconds")
        except ValueError as e:
            print(e)
    elif method == '2':
        d_brute_force, brute_force_time = crack_private_key_brute_force(public_key)
        if d_brute_force is not None:
            print("Private exponent (d) cracked using brute force method:", d_brute_force)
            print(f"Brute force runtime: {brute_force_time:.6f} seconds")
        else:
            print("Failed to crack the private exponent using brute force method.")
            print("Trying alternative methods...")
            try:
                p, q = factor_modulus(public_key[1])
                d_factorized = modular_inverse(public_key[0], (p - 1) * (q - 1))
                print("Private exponent (d) cracked using factorization method:", d_factorized)
            except ValueError as e:
                print("Failed to crack the private exponent using factorization method.")
                print("This can happen when the RSA key length is too large.")

if __name__ == "__main__":
    main()
