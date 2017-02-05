"""

This file is the place to write solutions for the
skills assignment called skills-sqlalchemy. Remember to
consult the exercise instructions for more complete
explanations of the assignment.

All classes from model.py are being imported for you
here, so feel free to refer to classes without the
[model.]User prefix.

"""

from model import *

init_app()


# -------------------------------------------------------------------
# Part 2: Discussion Questions


# 1. What is the datatype of the returned value of
# ``Brand.query.filter_by(name='Ford')``?
# BaseQuery. It is an object of the Query type. Still hasn't gone to the DB, it just has the order.


# 2. In your own words, what is an association table, and what type of
# relationship (many to one, many to many, one to one, etc.) does an
# association table manage?

# TODO: - Answer questions, checke the queries returning the data and not the objects. Function 2. Join ?
# TODO: Play with debug to see how many time a query is call in the comprehension (Func 1 and 2)


# -------------------------------------------------------------------
# Part 3: SQLAlchemy Queries


# Get the brand with the ``id`` of "ram."
q1 = db.session.query(Brand.name).filter(Brand.brand_id == 'ram').all()[0][0]   # or ...
q1 = Brand.query.filter(Brand.brand_id == 'ram').all()[0].name                  #or ...
q1 = Brand.query.filter(Brand.brand_id == 'ram').first().name

# Get all models with the name "Corvette" and the brand_id "che."
q2 = Model.query.filter(Model.name == 'Corvette').all()   # Since all Corvette are che, we could ommit filter by 'che'
q2 = Model.query.filter(Model.brand_id == 'che', Model.name == 'Corvette').all()    # this is what is asked though.

# Get all models that are older than 1960.
q3 = db.session.query(Model).filter(Model.year < 1960).all()        # or ...
q3 = Model.query.filter(Model.year < 1960).all()

# Get all brands that were founded after 1920.
q4 = db.session.query(Brand).filter(Brand.founded > 1920).all()     # or ...
q4 = Brand.query.filter(Brand.founded > 1920).all()

# Get all models with names that begin with "Cor."
q5 = db.session.query(Model).filter(Model.name.like('Cor%')).all()  # or ...
q5 = Model.query.filter(Model.name.like('Cor%')).all()

# Get all brands that were founded in 1903 and that are not yet discontinued.
q6 = db.session.query(Brand).filter(Brand.founded == 1903, Brand.discontinued.is_(None)).all()    # or ...
q6 = Brand.query.filter(Brand.founded == 1903, Brand.discontinued.is_(None)).all()                # or ...
q6 = Brand.query.filter((Brand.founded == 1903) & (Brand.discontinued.is_(None))).all()

# Get all brands that are either 1) discontinued (at any time) or 2) founded
# before 1950.
q7 = Brand.query.filter(db.or_(Brand.founded < 1950, Brand.discontinued.isnot(None))).all()     # or ...
q7 = Brand.query.filter((Brand.founded < 1950) | (Brand.discontinued.isnot(None))).all()


# Get any model whose brand_id is not "for."
q8 = Brand.query.filter(Brand.brand_id != 'for').all()



# -------------------------------------------------------------------
# Part 4: Write Functions


def get_model_info(year):
    """Takes in a year and prints out each model name, brand name, and brand
    headquarters for that year using only ONE database query."""

    # Add join to eagerly load ?
    models_for_year = db.session.query(Model).filter(Model.year == year).all()
    print [(model.name, model.brand.name, model.brand.headquarters) for model in models_for_year]
    


def get_brands_summary():
    """Prints out each brand name and each model name with year for that brand
    using only ONE database query."""

    # db.session.query(Model.brand.name, Model.name, Model.year).order_by(Model.brand_id).all()  #not seure od Model.brand.name
    # db.session.query(Model.name, Model.year).order_by(Model.brand_id).all() # Works

def search_brands_by_name(mystr):
    """Returns all Brand objects corresponding to brands whose names include
    the given string."""

    partial_brand = '%%%s%%' % mystr
    
    return Brand.query.filter(Brand.name.like(partial_brand)).all()


def get_models_between(start_year, end_year):
    """Returns all Model objects corresponding to models made between
    start_year (inclusive) and end_year (exclusive)."""

    return Model.query.filter(Model.year >= start_year, Model.year < end_year).all()

