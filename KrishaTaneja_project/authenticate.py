from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from PIL import Image
import hashlib
import sys
import os

def generate_keys():
    """generate RSA key pair for signing"""
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()
    
    with open("camera_private.pem", "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))
    
    with open("camera_public.pem", "wb") as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))
    
    print("Keys generated: camera_private.pem, camera_public.pem")

def hash_image(image_path):
    """create SHA-256 hash"""
    sha256_hash = hashlib.sha256()
    with open(image_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.digest()

def sign_image(image_path):
    """signing an image + save signature separately"""
    # Load private key
    with open("camera_private.pem", "rb") as f:
        private_key = serialization.load_pem_private_key(f.read(), password=None)
    
    image_hash = hash_image(image_path)
    

    signature = private_key.sign(
        image_hash,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    
    sig_path = image_path + ".sig"
    with open(sig_path, "wb") as f:
        f.write(signature)
    
    print(f"  Image signed: {sig_path}")
    print(f"  Hash: {image_hash.hex()[:32]}...")
    print(f"  Signature: {signature.hex()[:32]}...")

def verify_image(image_path):

    with open("camera_public.pem", "rb") as f:
        public_key = serialization.load_pem_public_key(f.read())
    
    sig_path = image_path + ".sig"
    if not os.path.exists(sig_path):
        print("NO SIGNATURE FOUND")
        return False
    
    with open(sig_path, "rb") as f:
        signature = f.read()
    
    image_hash = hash_image(image_path)
    
    try:
        public_key.verify(
            signature,
            image_hash,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        print(f"  AUTHENTIC")
        print(f"  Image hash: {image_hash.hex()[:32]}...")
        return True
    except:
        print("TAMPERED")
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 authenticate.py generate        - Generate keys")
        print("  python3 authenticate.py sign <image>    - Sign an image")
        print("  python3 authenticate.py verify <image>  - Verify an image")
        return
    
    command = sys.argv[1]
    
    if command == "generate":
        generate_keys()
    
    elif command == "sign":
        if len(sys.argv) < 3:
            print("Error: Provide image path")
            return
        image_path = sys.argv[2]
        if not os.path.exists(image_path):
            print(f"Error: {image_path} not found")
            return
        sign_image(image_path)
    
    elif command == "verify":
        if len(sys.argv) < 3:
            print("Error: Provide image path")
            return
        image_path = sys.argv[2]
        if not os.path.exists(image_path):
            print(f"Error: {image_path} not found")
            return
        verify_image(image_path)
    
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()