import bcrypt


def encrypt( password: str ) -> str:
    encoding = 'utf-8'
    byte_pw = bytes( password, encoding )

    salt = bcrypt.gensalt()
    hashed_pw = bcrypt.hashpw( byte_pw, salt )

    salt_str = salt.decode( encoding )
    hashed_pw_str = hashed_pw.decode( encoding )

    return hashed_pw_str


def validate( input_pw: str, db_pw: str ) -> bool:
    encoding = 'utf-8'
    salt = db_pw[:29]
    db_extracted_pw = db_pw[29:]

    hashed_input_pw = bcrypt.hashpw( bytes( input_pw, encoding ), bytes( salt, encoding ) )
    hashed_input_pw_str = hashed_input_pw.decode( encoding )

    if hashed_input_pw_str == db_pw:
        return True

    return False