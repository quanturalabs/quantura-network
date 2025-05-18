# pqcrypto/dilithium_example.py

from pqcrypto.sign.dilithium2 import generate_keypair, sign, verify
import base64

def demo():
    # Generate a post-quantum keypair (Dilithium2)
    public_key, secret_key = generate_keypair()

    message = b"Hello from Quantura – secure and post-quantum!"

    # Sign the message
    signature = sign(message, secret_key)

    # Verify the signature
    try:
        verify(message, signature, public_key)
        print("✅ Signature verified (post-quantum safe).")
    except Exception as e:
        print("❌ Signature verification failed:", e)

if __name__ == "__main__":
    demo()

