from flask import ( 
    Blueprint, flash, render_template, request, url_for, redirect
) 
from .models import Car,User
from .forms import carForm, carChangeForm
from . import db
from flask_login import login_required, current_user


#create a blueprint
bp = Blueprint('cars', __name__, url_prefix='/cars')

@bp.route('/<id>') 
def show(id): 
  car = Car.query.filter_by(sold='yes',id=id).first()  
  return render_template('cars/show.html', car=car)



@bp.route('/sold/<id>', methods = ['GET', 'POST'])
def sold(id):
  car = Car.query.filter_by(sold='yes', id=id).first()  

  return render_template('cars/sold.html', car=car)


@bp.route('/create', methods = ['GET', 'POST'])
def create():
  form = carForm()
  print('Method type: ', request.method)
  if form.validate_on_submit():
    print('Successfully created new car', 'success')
    # access the values in the form data
    carlisting = Car(
                user_id=current_user.name,
                name=form.name.data, 
                minprice=form.minprice.data,
                odometer=form.odometer.data,
                description=form.description.data,
                image=form.image.data)
    # add the object to the db session
    db.session.add(carlisting)
    # commit to the database
    db.session.commit()
    
    return redirect(url_for('main.index'))

  return render_template('cars/create.html', form=form)


@bp.route('/edit/<id>', methods = ['GET', 'POST'])
def edit(id): 
  car = Car.query.filter_by(id=id).first() 
  form = carChangeForm()

  print('Method type: ', request.method)
  if form.validate_on_submit():
    print('Successfully changed car details', 'success')
    # access the values in the form data
    car.name=form.name.data
    car.minprice=form.minprice.data
    car.odometer=form.odometer.data
    car.description=form.description.data
    car.image=form.image.data
    car.sold=form.sold.data

    db.session.add(car)

    # commit to the database
    db.session.commit()
  
    return redirect(url_for('main.index'))

  return render_template('cars/edit.html', car=car, form=form)




    