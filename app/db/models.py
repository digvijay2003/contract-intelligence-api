"""Database models for Contract Intelligence API"""
from sqlalchemy import Column, String, Integer, DateTime, Text, JSON, Float, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

Base = declarative_base()


class DocumentStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class RiskSeverity(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Document(Base):
    """Stores uploaded contract PDFs and their metadata"""
    __tablename__ = "documents"

    id = Column(String, primary_key=True)
    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    file_size = Column(Integer)
    mime_type = Column(String)
    
    status = Column(SQLEnum(DocumentStatus), default=DocumentStatus.PENDING)
    
    full_text = Column(Text)
    page_count = Column(Integer)
    
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    processed_at = Column(DateTime)
    
    extracted_fields = relationship("ExtractedField", back_populates="document", cascade="all, delete-orphan")
    audit_findings = relationship("AuditFinding", back_populates="document", cascade="all, delete-orphan")
    chunks = relationship("DocumentChunk", back_populates="document", cascade="all, delete-orphan")


class ExtractedField(Base):
    """Stores structured fields extracted from contracts"""
    __tablename__ = "extracted_fields"

    id = Column(Integer, primary_key=True, autoincrement=True)
    document_id = Column(String, ForeignKey("documents.id", ondelete="CASCADE"))
    
    parties = Column(JSON)  
    effective_date = Column(String)
    term = Column(String)
    governing_law = Column(String)
    payment_terms = Column(Text)
    termination = Column(Text)
    auto_renewal = Column(String)
    confidentiality = Column(Text)
    indemnity = Column(Text)
    liability_cap_amount = Column(Float)
    liability_cap_currency = Column(String)
    signatories = Column(JSON)  
    
    extracted_at = Column(DateTime, default=datetime.utcnow)
    extraction_model = Column(String)
    
    document = relationship("Document", back_populates="extracted_fields")


class AuditFinding(Base):
    """Stores risk findings from contract audits"""
    __tablename__ = "audit_findings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    document_id = Column(String, ForeignKey("documents.id", ondelete="CASCADE"))
    
    rule_id = Column(String)
    rule_name = Column(String)
    severity = Column(SQLEnum(RiskSeverity))
    description = Column(Text)
    
    evidence_text = Column(Text)
    page_number = Column(Integer)
    char_start = Column(Integer)
    char_end = Column(Integer)
    
    detected_at = Column(DateTime, default=datetime.utcnow)
    
    document = relationship("Document", back_populates="audit_findings")


class DocumentChunk(Base):
    """Stores text chunks for RAG retrieval"""
    __tablename__ = "document_chunks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    document_id = Column(String, ForeignKey("documents.id", ondelete="CASCADE"))
    
    chunk_index = Column(Integer)
    text = Column(Text)
    
    page_number = Column(Integer)
    char_start = Column(Integer)
    char_end = Column(Integer)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    document = relationship("Document", back_populates="chunks")


class QueryLog(Base):
    """Logs user queries for analytics"""
    __tablename__ = "query_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String)
    
    question = Column(Text)
    answer = Column(Text)
    document_ids = Column(JSON)
    
    latency_ms = Column(Integer)
    
    created_at = Column(DateTime, default=datetime.utcnow)