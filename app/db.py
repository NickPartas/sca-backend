from sqlmodel import SQLModel, create_engine
engine = create_engine("sqlite:///sca.db", echo=False)