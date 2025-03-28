from sqlalchemy.ext.declarative import declarative_base, declared_attr
import humps

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True
    # __table_args__ = {'schema': 'my_tests'}

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return humps.depascalize(cls.__name__)

