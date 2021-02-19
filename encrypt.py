import getopt
import sys
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP


def encrypt(data):

    file_out = open("encrypted_data.bin", "wb")

    recipient_key = RSA.import_key(open("receiver.pem").read())
    session_key = get_random_bytes(16)

    # Encrypt the session key with the public RSA key
    cipher_rsa = PKCS1_OAEP.new(recipient_key)
    enc_session_key = cipher_rsa.encrypt(session_key)

    # Encrypt the data with the AES session key
    cipher_aes = AES.new(session_key, AES.MODE_GCM)
    ciphertext, tag = cipher_aes.encrypt_and_digest(data)
    [file_out.write(x) for x in (enc_session_key, cipher_aes.nonce, tag, ciphertext)]
    file_out.close()


def get_args(argv):
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv, "hi:i:", ["ifile="])
    except getopt.GetoptError:
        print('test.py -i <inputfile> ')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('test.py -i <inputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg

    return inputfile


if __name__ =='__main__':
    inputf=get_args(sys.argv[1:]);
    with open(inputf, mode='rb') as file:
        fileContent = file.read()
    encrypt(fileContent)