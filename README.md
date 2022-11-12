# hmac
 
 1. Генератор тестов для протокола. 
 
 Открытый текст берется из файла input.txt. 
 
 python [FUNC] [PASSWORD] [HASH_FUNC] [ENC_FUNC]
 
    python generator.py -p 0a0b0cff --hash md5 -a aes192
    python generator.py -p 0a0b0cff --hash md5 -a aes256
    
 После запуска создается файл с расширением .enc (в этой же директории). Например для вышеуказанных примеров создаются 2 файла:
    md5_3des_0a0b0cff.enc 
    sha1_aes256_ffffffff.enc
    
 2. Верификатор для файлов протокола.

    Верификатор определяет, действительно ли файл содержит данные, соответствующие вышеописанному протоколу (ENC префикс, байты идентификаторов, NONCE, IV        и тд.).
    • 0-2 байты: буквы «ENC» в кодировке ASCII;
    • 3 байт: идентификатор хеш-функции (0 — MD5, 1 — SHA-1);
    • 4 байт: идентификатор алгоритма шифрования (0 — 3DES, 1 — AES-128, 2 —
    AES-192, 3 — AES-256);
    • 5 байт и далее: NONCE (64 байта), IV (в зависимости от размера блока алгоритма
    шифрования), шифртекст (длиной не более 4096 байт).
    
    python [FUNC] [FILENAME]
    
    python verifier.py --filename md5_aes128_000004ff.enc
    
    ответ:
    True
    
 3. Утилита подбора пароля для файла данного протокола. На вход подается только имя файла с расширением .enc.
  
  
    python [FUNC] [FILENAME]
    
    python cracking.py --filename md5_aes256_000b0cff.enc -v
    
      
    HMAC:  md5   aes256
    NONCE:  b'VdOlsJnJkrvEqVRabPkhNpaBBdNmRplQqwSMPFhoYhonjXWiAIHWayCVLZndwZOy'
    IV:  b'vAgZnoIKUILGEOQM'
    CT:  ebdb91249b6baa648a820b0914521bb43f68d8093010b4a3dabb2f3449da877b
    Start cracking ::
         Current:  bytearray(b'\x00\x00\x00\x00')  -  b'\x00\x00\xd3\xe0'  | Speed:  0.0  c/s... 
         Current:  b'\x00\x00\xd3\xe0'  -  b'\x00\x01\xa7\xc0'  | Speed:  40396.18774877053  c/s... 
         Current:  b'\x00\x01\xa7\xc0'  -  b'\x00\x02{\xa0'  | Speed:  40290.98339986834  c/s... 
         Current:  b'\x00\x02{\xa0'  -  b'\x00\x03O\x80'  | Speed:  40046.327597345255  c/s... 
         Current:  b'\x00\x03O\x80'  -  b'\x00\x04#`'  | Speed:  39939.891346363125  c/s... 
         Current:  b'\x00\x04#`'  -  b'\x00\x04\xf7@'  | Speed:  39915.40092091093  c/s... 
         Current:  b'\x00\x04\xf7@'  -  b'\x00\x05\xcb '  | Speed:  39957.72407580325  c/s... 
         Current:  b'\x00\x05\xcb '  -  b'\x00\x06\x9f\x00'  | Speed:  39988.616385326844  c/s... 
         Current:  b'\x00\x06\x9f\x00'  -  b'\x00\x07r\xe0'  | Speed:  39972.51266991189  c/s... 
         Current:  b'\x00\x07r\xe0'  -  b'\x00\x08F\xc0'  | Speed:  39995.111114696636  c/s...
         Current:  b'\x00\x08F\xc0'  -  b'\x00\t\x1a\xa0'  | Speed:  40014.75802508561  c/s...
         Current:  b'\x00\t\x1a\xa0'  -  b'\x00\t\xee\x80'  | Speed:  40019.83038557465  c/s...
         Current:  b'\x00\t\xee\x80'  -  b'\x00\n\xc2`'  | Speed:  40024.91506428277  c/s...
         Current:  b'\x00\n\xc2`'  -  b'\x00\x0b\x96@'  | Speed:  40040.13583782869  c/s...
          
         Found password! b'\x00\x0b\x0c\xff'  | Speed:  40044.05746587991  c/s...

