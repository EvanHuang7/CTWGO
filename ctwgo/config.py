class Config:
    SECRET_KEY = 'af6103e4c8f6e7f2a1e72b2b58730cc6'

    # "///" specify a relative path, same directary as application
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'

    # Google's Gmail SMTP server
    MAIL_SERVER = 'smtp.googlemail.com'

    # Port for TLS Outgoing Mail (SMTP) Server
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    
    MAIL_USERNAME = 'robotcs1987@gmail.com'
    MAIL_PASSWORD = 'robotcs123'
    