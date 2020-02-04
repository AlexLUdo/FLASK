from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///xx.sqlite',  connect_args={'check_same_thread': False})

Base = declarative_base()

class Vacancy(Base):
    __tablename__ = 'zapros'
    id = Column(Integer, primary_key=True)
    vac = Column(String)
    reg = Column(String)
    num = Column(Integer)
  
    def __init__(self, vac, reg, num):
        self.vac = vac
        self.reg = reg
        self.num = num

    def __str__(self):
        return f'{self.id} {self.vac} {self.reg}  {self.num}'


class Skill(Base):
    __tablename__ = 'skills'
    id = Column(Integer, primary_key=True)
    skl = Column(String)
    reg = Column(String)


    def __init__(self, skl, reg):
        self.skl = skl
        self.reg = reg

    def __str__(self):
        return f'{self.id} {self.skl} {self.reg}'

def put(vac, reg, num, vse_skily):
    skl = list({name: dict.keys for name in dict.keys(vse_skily)})
    skl = str(skl)
    Session = sessionmaker(bind=engine)
    session = Session()
    vacancy = Vacancy(vac, reg, num)
    skills = Skill(skl, reg)
    session.add(vacancy)
    session.add(skills)
    session.commit()


def get(area, vacanc):
    Session = sessionmaker(bind=engine)
    session = Session()
    vacancies = session.query(Vacancy.vac,Vacancy.reg,Vacancy.num).filter(Vacancy.vac == vacanc, Vacancy.reg == area).all()
    return vacancies
