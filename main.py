

# 1)a) create a fast api application on given data set. Need to have four end points
# 		POST    /candidates ---> Add a new candidate
# 		GET     /candidates ---> Read all candidates
# 		PUT     /candidates/{id} ---> Modify a candidate
# 		DELETE  /candidates/{id} ---> Delete a candidate
		
#    - add email & phone numbers to each candidate with proper validations.
#    - filter and show candidates with above 40 marks in maths and history
#    - Add random 3 students to dataset
#    - integrate SQL and transfter data set into sql (use any of your choice).
#    - End points should work in all systems.
   
#   b) Explain about Authentication in FastAPI and explain how can you allow only admin to access student detais?

#candidates FASTAPI#

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from typing import Optional, List
import random
import re





DATABASE_URL = "mysql+pymysql://root:Jaswanth09@127.0.0.1:3306/candidates"

    
engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

# MODEL


class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True)
    phone = Column(String(15))
    maths_marks = Column(Integer)
    history_marks = Column(Integer)


Base.metadata.create_all(bind=engine)

# VALIDATION


def validate_phone(phone: str):
    if not re.fullmatch(r"[6-9]\d{9}", phone):
        raise ValueError("Invalid Indian phone number")
    return phone



# SCHEMAS


class CandidateCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str
    maths_marks: int = Field(ge=0, le=100)
    history_marks: int = Field(ge=0, le=100)


class CandidateUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    maths_marks: Optional[int] = None
    history_marks: Optional[int] = None


class CandidateResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: str
    maths_marks: int
    history_marks: int

    class Config:
        from_attributes = True


# DB DEPENDENCY


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# FASTAPI APP


app = FastAPI(title="My Candidate API")


@app.get("/")
def read():
    return{"FASTAPI IS RUNNING GOOD "}


@app.post("/candidates", response_model=CandidateResponse)
def create_candidate(candidate: CandidateCreate,
                     db: Session = Depends(get_db)):

    validate_phone(candidate.phone)

    existing = db.query(Candidate)\
                 .filter(Candidate.email == candidate.email)\
                 .first()

    if existing:
        raise HTTPException(400, "Email already exists")

    obj = Candidate(**candidate.model_dump())

    db.add(obj)
    db.commit()
    db.refresh(obj)

    return obj



@app.get("/candidates",
         response_model=List[CandidateResponse])
def get_candidates(high_scorers: bool = False,
                   db: Session = Depends(get_db)):

    query = db.query(Candidate)

    if high_scorers:
        query = query.filter(
            Candidate.maths_marks > 40,
            Candidate.history_marks > 40
        )

    return query.all()


@app.put("/candidates/{candidate_id}",
         response_model=CandidateResponse)
def update_candidate(candidate_id: int,
                     candidate: CandidateUpdate,
                     db: Session = Depends(get_db)):

    db_candidate = db.query(Candidate)\
                     .filter(Candidate.id == candidate_id)\
                     .first()

    if not db_candidate:
        raise HTTPException(404, "Candidate not found")

    for key, value in candidate.model_dump(
            exclude_unset=True).items():
        setattr(db_candidate, key, value)

    db.commit()
    db.refresh(db_candidate)

    return db_candidate

@app.delete("/candidates/{candidate_id}")
def delete_candidate(candidate_id: int,
                     db: Session = Depends(get_db)):

    obj = db.query(Candidate)\
            .filter(Candidate.id == candidate_id)\
            .first()

    if not obj:
        raise HTTPException(404, "Candidate not found")

    db.delete(obj)
    db.commit()

    return {"message": "Deleted Successfully"}
# ADD RANDOM 3 STUDENTS


@app.post("/candidates/random")
def add_random_students(db: Session = Depends(get_db)):

    names = ["Alex", "John", "Ravi", "Kiran", "Sneha"]

    for _ in range(3):
        student = Candidate(
            name=random.choice(names),
            email=f"user{random.randint(1,9999)}@mail.com",
            phone=f"9{random.randint(100000000,999999999)}",
            maths_marks=random.randint(30,100),
            history_marks=random.randint(30,100)
        )
        db.add(student)

    db.commit()

    return {"message": "3 Random Students Added"}

