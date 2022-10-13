import logging
import flask
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from ml_api_milvus.api.config import Config

_logger = logging.getLogger(__name__)

# Base class for SQLAlchemy models
Base = declarative_base()

from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func

from ml_api_milvus.api.persistence.core import Base


class LiveModelPredictions(Base):
    """
    Schema for Live Model
    """
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

def create_db_engine_from_config(*, config: Config) -> Engine:
    """The Engine is the starting point for any SQLAlchemy application.
    """

    engine = create_engine(config.SQLALCHEMY_DATABASE_URI,)

    _logger.info(f"creating DB conn with URI: {config.SQLALCHEMY_DATABASE_URI}")
    return engine


def create_db_session(*, engine: Engine) -> scoped_session:
    """The Session establishes all conversations with the database.
     """
    return scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=engine,),
    )


def init_database(app: Flask, config: Config, db_session=None) -> None:
    """Connect to the database and attach DB session to the app."""

    if not db_session:
        engine = create_db_engine_from_config(config=config)
        db_session = create_db_session(engine=engine)

    Base.metadata.create_all(engine)
    #app.g.db_session = db_session

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()
    
    return db_session