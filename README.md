# Image Authentication System

A cryptographic image authentication system that uses SHA-256 hashing and RSA digital signatures to verify image authenticity and detect tampering.

## Overview

This project explores how cryptographic techniques can be used to establish trust in digital images. Instead of relying on metadata or manual inspection, images are authenticated through digital signatures that can be verified using a public key.

## Features

- SHA-256 image hashing
- RSA-2048 digital signatures
- Image authenticity verification
- Tampering detection
- Protection against signature replay attacks
- Detection of unsigned or AI-generated content

## Security Scenarios Tested

| Scenario | Result |
|-----------|----------|
| Authentic signed image | AUTHENTIC |
| Unsigned image | NO SIGNATURE FOUND |
| Modified image | TAMPERED |
| Signature replay attack | TAMPERED |

## Technologies

- Python
- RSA-2048
- SHA-256
- Public Key Cryptography
