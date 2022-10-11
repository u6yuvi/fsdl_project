from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func

from api.persistence.core import Base


class LiveModelPredictions(Base):
    __tablename__ = "clip_model_predictions"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    user_id = Column(String(36), nullable=False)
    datetime_captured = Column(
        DateTime(timezone=True), server_default=func.now(), index=True
    )
    model_version = Column(String(36), nullable=False)
    inputs = Column(JSONB)
    outputs = Column(JSONB)


# class ShadowModelPredictions(Base):
#     raise NotImplementedError