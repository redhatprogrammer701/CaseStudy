from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import pandas as pd

app = Flask(__name__)
engine = create_engine('sqlite:///Articles-Manager.db')

Base = declarative_base()

class Article(Base):
    __tablename__ = 'Articulos'
    
    id_ = Column(Integer, primary_key=True, autoincrement=True)
    Date = Column(String(50), nullable=False, default=datetime.utcnow)        
    Title = Column(String(250), nullable=False)
    Tag = Column(String(250), nullable=False)
    Resume = Column(String(250), nullable=False)
    Link = Column(String(400), nullable=False)


Base.metadata.create_all(engine)

df = pd.read_csv("valores.csv")
df.to_sql('Articulos', engine, if_exists='replace', index=False)

session = sessionmaker()
session.configure(bind=engine)
s = session()

results = s.query(Article).all()
@app.route('/')
def index():
    return render_template('index.html', results=results)

if __name__ == "__main__":
    app.run(debug=True)