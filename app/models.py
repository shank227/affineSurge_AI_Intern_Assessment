from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    version = Column(String, nullable=False)

    sections = relationship("Section", back_populates="document")


class Section(Base):
    __tablename__ = "sections"

    id = Column(Integer, primary_key=True, index=True)

    document_id = Column(Integer, ForeignKey("documents.id"))

    section_number = Column(String)
    title = Column(String)
    level = Column(Integer)
    parent_section = Column(String)

    content = Column(Text)

    document = relationship("Document", back_populates="sections")