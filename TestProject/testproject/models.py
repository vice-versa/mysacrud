from sqlalchemy import (
    Column,
    Integer,
    Text,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    backref, relationship)

from zope.sqlalchemy import ZopeTransactionExtension
from sqlalchemy.types import String, Enum, Boolean, Float
from sacrud.position import before_insert
from sqlalchemy.event import listen
from sqlalchemy.schema import ForeignKey
from sacrud.exttype import FileStore
from sacrud.tests.test_models import PHOTO_PATH

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class User(Base):

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)
    position = Column(Integer, default=0)
    sex = Column(Enum('male',
                      'female',
                      'alien',
                      'unknown',
                       name="sex"))

    def __init__(self, name, fullname, password, position=0,
                       sex='unknown'):
        self.name = name
        self.fullname = fullname
        self.password = password
        self.position = position
        self.sex = sex

    def __repr__(self):
        return "<User('%s','%s', '%s')>" % (self.name,
                                            self.fullname,
                                            self.password)


listen(User, "before_insert", before_insert)
listen(User, "before_update", before_insert)


class Profile(Base):

    __tablename__ = 'profile'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    user = relationship(User, backref=backref("profile", lazy="joined"))
    phone = Column(String)
    cv = Column(Text)
    married = Column(Boolean)
    salary = Column(Float)
    photo = Column(FileStore(path="/assets/photo", abspath=PHOTO_PATH))

    def __init__(self, user, phone="", cv="", married=False, salary=20.0):
        self.user = user
        self.phone = phone
        self.cv = cv
        self.married = married
        self.salary = salary

    def __repr__(self):
        return "<Profile of user '%s'" % ((self.user, ))

    def set_photo(self, value):
        self.photo = value
