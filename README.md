# hmac
 
 ##1. Генератор тестов для протокола. 
 
 Открытый текст берется из файла input.txt. 
 
 python [FUNC] [PASSWORD] [HASH_FUNC] [ENC_FUNC]
 
    python --func=gen --pass=0a0b0cff --hash=md5 --enc=3des
    python --func=gen --pass=ffffffff --hash=sha1 --enc=aes256
    
 После запуска создается файл с расширением .enc (в этой же директории). Например для вышеуказанных примеров создаются 2 файла:
    md5_3des_0a0b0cff.enc 
    sha1_aes256_ffffffff.enc
    
 ##2. Верификатор для файлов протокола.
