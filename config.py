# -*- coding: utf-8 -*-
import os

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
#DEBUG = True
#ENVIRONMENT = 'development'


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = "Jxd6x1dx7f0x11Bx]d4x+92dxaax{9aDxb3fJcwxd6};xd1Hxfcm;xc3xdbw,4xc0]x1f"


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
