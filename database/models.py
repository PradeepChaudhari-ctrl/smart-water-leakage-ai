from sqlalchemy import Column, Integer, Float, String
from database.db import Base


class Prediction(Base):

    __tablename__ = "predictions"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    filename = Column(
        String
    )

    status = Column(
        String
    )

    probability = Column(
        Float
    )

    severity = Column(
        String
    )