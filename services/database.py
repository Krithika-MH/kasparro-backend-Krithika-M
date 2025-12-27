# services/database.py

from sqlalchemy import create_engine, Column, Integer, String, DateTime, JSON, Float, Boolean, text
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timezone
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://kasparro:password@127.0.0.1:5433/kasparro")

engine = create_engine(DATABASE_URL, echo=False)  # Set echo=False to reduce logs
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# ==================== DATABASE TABLES ====================

class RawAPIData(Base):
    __tablename__ = "raw_api_data"
    id = Column(Integer, primary_key=True, autoincrement=True)
    source = Column(String(50), nullable=False)
    raw_data = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class RawCSVData(Base):
    __tablename__ = "raw_csv_data"
    id = Column(Integer, primary_key=True, autoincrement=True)
    raw_data = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class CleanedData(Base):
    __tablename__ = "cleaned_data"
    id = Column(Integer, primary_key=True, autoincrement=True)
    data_source = Column(String(50), nullable=False)
    crypto_id = Column(String(100))
    crypto_name = Column(String(100))
    price_usd = Column(Float)
    market_cap_usd = Column(Float, nullable=True)
    volume_24h_usd = Column(Float, nullable=True)
    change_24h_percent = Column(Float, nullable=True)
    normalized_data = Column(JSON)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class ETLCheckpoint(Base):
    __tablename__ = "etl_checkpoints"
    id = Column(Integer, primary_key=True, autoincrement=True)
    source = Column(String(50), unique=True, nullable=False)
    last_processed_id = Column(Integer, default=0)
    last_processed_timestamp = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class ETLRun(Base):
    __tablename__ = "etl_runs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    started_at = Column(DateTime, nullable=False)
    ended_at = Column(DateTime, nullable=True)
    records_processed = Column(Integer, default=0)
    success = Column(Boolean, default=False)
    error_message = Column(String, nullable=True)
    source = Column(String(50), nullable=True)


# ==================== HELPER FUNCTIONS ====================

def init_db():
    """Initialize database - create all tables"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables created successfully!")

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_connection():
    """Test if database connection works"""
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))  # Fixed: use text() wrapper
        db.close()
        print("✓ Database connection successful!")
        return True
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        return False


# ==================== RUN THIS TO TEST ====================

# Add this at the very bottom of services/database.py

# Add this at the END of services/database.py (after all class definitions)

if __name__ == "__main__":
    print("=" * 60)
    print("🔧 INITIALIZING DATABASE TABLES")
    print("=" * 60)
    
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully!")
        
        # Verify tables were created
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        print(f"\n📋 Tables created ({len(tables)} total):")
        for table in tables:
            print(f"   ✓ {table}")
        
        print("\n" + "=" * 60)
        print("✅ DATABASE INITIALIZATION COMPLETE")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ ERROR CREATING TABLES:")
        print(f"   {str(e)}")
        print("=" * 60)
        raise
