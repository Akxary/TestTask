from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, TIMESTAMP, DATE, DECIMAL
from sqlalchemy.orm import relationship
from db_connect import Base


class Agrmnt(Base):
    __tablename__ = "agrmnt"
    id = Column(Integer, primary_key=True, autoincrement=True)
    number = Column(Integer, unique=True, nullable=False)
    male = Column(String, nullable=False)
    birth_date = Column(DATE, nullable=False)
    retirement_years = Column(Integer, nullable=False)
    # связь с классом Базовая Пенсия по полю base_retirement.agrmnt (поля нет в db)
    base_retirement = relationship("BaseRetirement", back_populates="agrmnt")
    # связь с классом Платеж по полю agrmnt.payment
    payment = relationship("Payment", back_populates="agrmnt")


class BaseRetirement(Base):
    __tablename__ = "base_retirement"
    id = Column(Integer, primary_key=True, autoincrement=True)
    agrmnt_id = Column(Integer, ForeignKey("agrmnt.id"), nullable=False)
    base_retirement = Column(DECIMAL, nullable=False)
    # связь с классом договор по полю agrmnt.base_retirement (поля нет в db)
    agrmnt = relationship("Agrmnt", back_populates="base_retirement")


class Payment(Base):
    __tablename__ = "payment"
    id = Column(Integer, primary_key=True, autoincrement=True)
    agrmnt_id = Column(Integer, ForeignKey("agrmnt.id"), nullable=False)
    payment_date = Column(DATE, nullable=False)
    amount = Column(DECIMAL, nullable=False)
    # связь с классом договор по полю agrmnt.payment (поля нет в db)
    agrmnt = relationship("Agrmnt", back_populates="payment")


# Base.metadata.create_all(bind=engine)
