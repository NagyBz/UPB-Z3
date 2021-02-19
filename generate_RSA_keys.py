from Crypto.PublicKey import RSA

if __name__ == '__main__':
    key = RSA.generate(2048)
    private_key = key.export_key()
    file_out = open("private.pem", "wb")
    file_out.write(private_key)
    file_out.close()
    print("private key saved into file : private.pem")

    public_key = key.publickey().export_key()
    file_out = open("receiver.pem", "wb")
    file_out.write(public_key)
    file_out.close()
    print("public key saved into file : public.pem")