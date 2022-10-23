# hmac
 
 1. Генератор тестов для протокола. 
 
 Открытый текст берется из файла input.txt. 
 
 python [FUNC] [PASSWORD] [HASH_FUNC] [ENC_FUNC]
 
    python --func=gen --pass=0a0b0cff --hash=md5 --enc=3des
    python --func=gen --pass=ffffffff --hash=sha1 --enc=aes256
    
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
    
    python --func=ver --file=md5_3des_0a0b0cff.enc 
    
    ответ:
    True
    
 3. Утилита подбора пароля для файла данного протокола. На вход подается только имя файла с расширением .enc.
  
  
    python [FUNC] [FILENAME]
    
    python --func=crack --filename=md5_3des_01020304.enc
    
    Valid file!
    HMAC_MD5, 3DES
    NONCE: 23748f19...
    IV: 01d839f8...
    CT: 23d910f8...
    Start cracking
    Current: 00000000-0000ffff
    Current: 0000ffff-0001fffe | Speed: 1000 c/s... Current: 0001fffe-0002fffd | Speed: 1300 c/s...
