"""
Schema and Related Models - PHASE 1
Represents database schemas, tables, and columns
"""

from datetime import datetime
from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Integer, Text, Enum
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY
from sqlalchemy.orm import relationship
from uuid import uuid4
import enum
from app.database.connection import Base

class Schema(Base):
    """
    Schema Model
    Represents a database schema
    """
    __tablename__ = "schemas"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    
    # Foreign Keys
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True)
    database_id = Column(UUID(as_uuid=True), ForeignKey("databases.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Schema Information
    schema_name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    
    # Metadata
    table_count = Column(Integer, default=0)
    total_columns = Column(Integer, default=0)
    
    # Documentation
    documentation = Column(Text, nullable=True)
    business_context = Column(Text, nullable=True)
    
    # Indexing
    is_indexed = Column(Boolean, default=False)
    vector_store_id = Column(String(255), nullable=True)  # Reference to Pinecone
    
    # Sync Status
    last_synced = Column(DateTime, nullable=True)
    sync_status = Column(String(50), default="pending")  # pending, syncing, synced, failed
    
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    tenant = relationship("Tenant", back_populates="schemas")
    database = relationship("Database", back_populates="schemas")
    tables = relationship("Table", back_populates="schema", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Schema(id={self.id}, schema_name={self.schema_name})>"

class Table(Base):
    """
    Table Model
    Represents a database table
    """
    __tablename__ = "tables"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    
    # Foreign Keys
    schema_id = Column(UUID(as_uuid=True), ForeignKey("schemas.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Table Information
    table_name = Column(String(255), nullable=False)
    display_name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    
    # Table Metadata
    row_count = Column(Integer, default=0)
    column_count = Column(Integer, default=0)
    
    # Documentation
    business_description = Column(Text, nullable=True)
    usage_examples = Column(JSONB, default=list)  # Examples of how to use this table
    
    # Access Control
    is_sensitive = Column(Boolean, default=False)  # Contains PII
    is_queryable = Column(Boolean, default=True)
    
    # Indexing
    is_indexed = Column(Boolean, default=False)
    vector_store_id = Column(String(255), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    schema = relationship("Schema", back_populates="tables")
    columns = relationship("Column", back_populates="table", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Table(id={self.id}, table_name={self.table_name})>"

class Column(Base):
    """
    Column Model
    Represents a database column
    """
    __tablename__ = "columns"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    
    # Foreign Keys
    table_id = Column(UUID(as_uuid=True), ForeignKey("tables.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Column Information
    column_name = Column(String(255), nullable=False)
    display_name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    
    # Data Type
    data_type = Column(String(50), nullable=False)  # VARCHAR, INT, DATETIME, etc.
    is_nullable = Column(Boolean, default=True)
    
    # Column Metadata
    is_primary_key = Column(Boolean, default=False)
    is_foreign_key = Column(Boolean, default=False)
    is_unique = Column(Boolean, default=False)
    is_indexed = Column(Boolean, default=False)
    
    # Business Metadata
    business_name = Column(String(255), nullable=True)
    business_description = Column(Text, nullable=True)
    semantic_type = Column(String(50), nullable=True)  # dimension, measure, date, category, etc.
    
    # Access Control
    is_sensitive = Column(Boolean, default=False)  # PII field
    is_queryable = Column(Boolean, default=True)
    
    # Relationships
    foreign_key_reference = Column(String(500), nullable=True)  # "schema.table.column"
    
    # Sample Values
    sample_values = Column(JSONB, default=list)  # For understanding the data
    
    # Ordering
    column_order = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    table = relationship("Table", back_populates="columns")
    
    def __repr__(self):
        return f"<Column(id={self.id}, column_name={self.column_name}, data_type={self.data_type})>"
