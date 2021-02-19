import getopt
import sys

from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP

def decrypt():
    try:
        file_in = open("encrypted_data.bin", "rb")

        private_key = RSA.import_key(open("private.pem").read())

        enc_session_key, nonce, tag, ciphertext = \
            [file_in.read(x) for x in (private_key.size_in_bytes(), 16, 16, -1)]

        # Decrypt the session key with the private RSA key
        cipher_rsa = PKCS1_OAEP.new(private_key)
        session_key = cipher_rsa.decrypt(enc_session_key)

        # Decrypt the data with the AES session key
        cipher_aes = AES.new(session_key, AES.MODE_GCM, nonce)
        data = cipher_aes.decrypt_and_verify(ciphertext, tag)

        print(data.decode("utf-8"))
        f = open('decrypted.txt', "w")
        f.write(str(data, encoding='utf-8'))
        f.close()
    except :
        print(" ValueError Exception : tampering detected")


def get_args(argv):
    inputfile = ''
    key = ''
    try:
        opts, args = getopt.getopt(argv, "hi:k:", ["ifile=", "kfile="])
    except getopt.GetoptError:
        print('test.py -i <inputfile> -k <key>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('test.py -i <inputfile> -k <key>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-k", "--kfile"):
            key = arg
    return inputfile,key

if __name__ == '__main__':
    decrypt()