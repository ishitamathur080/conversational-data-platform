"""
Query Model - PHASE 1
Represents query execution history and results
"""

from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Integer, Text, Enum, Float
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from uuid import uuid4
import enum
from app.database.connection import Base

class QueryStatus(str, enum.Enum):
    """Query execution status"""
    PENDING = "pending"
    ANALYZING = "analyzing"
    REWRITING = "rewriting"
    GENERATING = "generating"
    VALIDATING = "validating"
    EXECUTING = "executing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class Query(Base):
    """
    Query Model
    Represents a natural language query and its execution
    """
    __tablename__ = "queries"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    
    # Foreign Keys
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True)
    database_id = Column(UUID(as_uuid=True), ForeignKey("databases.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    
    # Query Content
    natural_language_query = Column(Text, nullable=False)
    original_query = Column(Text, nullable=True)  # User's original question
    
    # Query Processing
    analyzed_query = Column(Text, nullable=True)  # After analysis
    rewritten_query = Column(Text, nullable=True)  # After rewriting
    generated_sql = Column(Text, nullable=True)  # Generated SQL
    executed_sql = Column(Text, nullable=True)  # SQL actually executed
    
    # Context Used
    relevant_schemas = Column(JSONB, default=list)  # Schemas used for generation
    relevant_tables = Column(JSONB, default=list)  # Tables referenced
    relevant_context = Column(Text, nullable=True)  # Retrieved context from RAG
    
    # Execution Details
    status = Column(Enum(QueryStatus), default=QueryStatus.PENDING, index=True)
    execution_start_time = Column(DateTime, nullable=True)
    execution_end_time = Column(DateTime, nullable=True)
    execution_duration = Column(Float, nullable=True)  # milliseconds
    
    # Results
    result_row_count = Column(Integer, nullable=True)
    result_column_count = Column(Integer, nullable=True)
    results = Column(JSONB, nullable=True)  # Query results as JSON
    
    # Error Handling
    error_message = Column(Text, nullable=True)
    error_type = Column(String(100), nullable=True)
    is_error_corrected = Column(bool, default=False)
    correction_attempts = Column(Integer, default=0)
    
    # Clarification
    needs_clarification = Column(bool, default=False)
    clarification_questions = Column(JSONB, default=list)  # Array of clarification questions
    user_response = Column(Text, nullable=True)  # User's response to clarification
    
    # Permissions
    requires_permission_check = Column(bool, default=True)
    permission_check_passed = Column(bool, nullable=True)
    permission_check_message = Column(Text, nullable=True)
    
    # Metadata
    query_type = Column(String(50), nullable=True)  # select, aggregate, join, etc.
    complexity_score = Column(Float, nullable=True)  # 0-1 score of query complexity
    
    # Cost
    estimated_cost = Column(Float, nullable=True)
    actual_cost = Column(Float, nullable=True)
    
    # Logging
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    tenant = relationship("Tenant", back_populates="queries")
    database = relationship("Database", back_populates="queries")
    user = relationship("User")
    
    def __repr__(self):
        return f"<Query(id={self.id}, status={self.status}, user_id={self.user_id})>"
