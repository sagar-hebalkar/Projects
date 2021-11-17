from django.conf import settings
from rsa.key import PrivateKey, PublicKey
import wave, os, rsa

def encodeAudio(audio_file,secret_text,public_key):
    ###Encrypting Secret Text With RSA Algorithm Before Hiding Message Into Audio File
    try:
        public_key = list(map(int,public_key.split(",")))
        public_key = PublicKey(*public_key)
        secret_text = secret_text.encode()
        cipher_text = rsa.encrypt(secret_text,public_key).hex()
    except:
        return None

    filename = "enc_"+audio_file.name
    audio = wave.open(audio_file, mode='rb')
    frame_bytes = bytearray(list(audio.readframes(audio.getnframes())))
    string = cipher_text + int((len(frame_bytes)-(len(cipher_text)*8*8))/8) *'#'
    bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8,'0') for i in string])))
    for i, bit in enumerate(bits):
        frame_bytes[i] = (frame_bytes[i] & 254) | bit
    frame_modified = bytes(frame_bytes)
    output_path = os.path.join(settings.MEDIA_ROOT,filename)
    with wave.open(output_path, 'wb') as fd:
        fd.setparams(audio.getparams())
        fd.writeframes(frame_modified)
    audio.close()
    return filename

def decodeAudio(audio_file,private_key):
    audio = wave.open(audio_file, mode='rb')
    frame_bytes = bytearray(list(audio.readframes(audio.getnframes())))
    extracted = [frame_bytes[i] & 1 for i in range(len(frame_bytes))]
    string = "".join(chr(int("".join(map(str,extracted[i:i+8])),2)) for i in range(0,len(extracted),8))
    cipher_text = string.split("###")[0]
    audio.close()

    ###Decrypting Secret Text With RSA Algorithm After Extrating Message From Audio File
    try:
        private_key = list(map(int,private_key.split(",")))
        private_key = PrivateKey(*private_key)
        cipher_text = bytes.fromhex(cipher_text)
        secret_text = rsa.decrypt(cipher_text,private_key)
        return secret_text.decode()
    except:
        return None