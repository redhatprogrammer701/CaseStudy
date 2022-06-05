from flask import Flask, render_template, request
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, desc
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import pandas as pd

app = Flask(__name__)
engine = create_engine('sqlite:///Articles-Manager.db', connect_args={'check_same_thread': False})

Base = declarative_base()

class Article(Base):
    __tablename__ = 'ARTICULOS'
    
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

@app.route('/', methods=['GET', 'POST'])
def index():
    results = s.query(Article).all()
    if request.method == 'POST' and 'tag' in request.form:
        tag = request.form["tag"]
        search = "%{}%".format(tag)
        results = s.query(Article).order_by(desc(Article.Date)).filter(Article.Tag.like(search)).all() 
        return render_template('index.html', results=results, tag=tag)
    return render_template('index.html', results=results)

if __name__ == "__main__":
    app.run(debug=True)