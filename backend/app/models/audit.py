"""
Audit Model - PHASE 1
For tracking all actions for compliance and security
"""

from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Enum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from uuid import uuid4
import enum
from app.database.connection import Base

class AuditActionType(str, enum.Enum):
    """Types of actions to audit"""
    # Authentication
    LOGIN = "login"
    LOGOUT = "logout"
    LOGIN_FAILED = "login_failed"
    
    # User Management
    USER_CREATED = "user_created"
    USER_UPDATED = "user_updated"
    USER_DELETED = "user_deleted"
    USER_ROLE_CHANGED = "user_role_changed"
    
    # Database Management
    DATABASE_ADDED = "database_added"
    DATABASE_UPDATED = "database_updated"
    DATABASE_DELETED = "database_deleted"
    DATABASE_CONNECTION_TESTED = "database_connection_tested"
    
    # Schema Management
    SCHEMA_SYNCED = "schema_synced"
    SCHEMA_UPDATED = "schema_updated"
    
    # Query Execution
    QUERY_EXECUTED = "query_executed"
    QUERY_FAILED = "query_failed"
    QUERY_CANCELLED = "query_cancelled"
    
    # Permission
    PERMISSION_DENIED = "permission_denied"
    UNAUTHORIZED_ACCESS_ATTEMPTED = "unauthorized_access_attempted"
    
    # Configuration
    CONFIG_CHANGED = "config_changed"
    RAG_INDEX_CREATED = "rag_index_created"
    RAG_INDEX_DELETED = "rag_index_deleted"
    
    # Security
    API_KEY_CREATED = "api_key_created"
    API_KEY_DELETED = "api_key_deleted"
    CREDENTIALS_UPDATED = "credentials_updated"

class AuditLog(Base):
    """
    Audit Log Model
    Comprehensive logging of all platform actions
    """
    __tablename__ = "audit_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    
    # Foreign Keys
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id", ondelete="CASCADE"), nullable=False, index=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="SET NULL"), nullable=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    
    # Action Details
    action_type = Column(Enum(AuditActionType), nullable=False, index=True)
    action_category = Column(String(50), nullable=False, index=True)  # auth, user, database, query, etc.
    action_description = Column(Text, nullable=False)
    
    # Resource Information
    resource_type = Column(String(100), nullable=True)  # User, Database, Query, etc.
    resource_id = Column(UUID(as_uuid=True), nullable=True, index=True)
    resource_name = Column(String(255), nullable=True)
    
    # Request Information
    request_ip = Column(String(45), nullable=True)  # IPv4 or IPv6
    request_user_agent = Column(String(500), nullable=True)
    request_method = Column(String(20), nullable=True)  # GET, POST, etc.
    request_path = Column(String(500), nullable=True)
    
    # Status
    action_status = Column(String(50), default="success")  # success, failure, warning
    status_code = Column(int, nullable=True)  # HTTP status code
    
    # Changes
    old_values = Column(JSONB, nullable=True)  # For updates
    new_values = Column(JSONB, nullable=True)  # For updates
    changes_summary = Column(Text, nullable=True)
    
    # Performance
    execution_time = Column(float, nullable=True)  # milliseconds
    
    # Timestamp
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    company = relationship("Company", back_populates="audit_logs")
    
    def __repr__(self):
        return f"<AuditLog(id={self.id}, action_type={self.action_type}, timestamp={self.timestamp})>"
