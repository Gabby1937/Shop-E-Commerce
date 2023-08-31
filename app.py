from flask import Flask, render_template, url_for, redirect, request, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.utils import secure_filename

# stage your app
app = Flask(__name__)

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}
UPLOAD_FOLDER = './static/images'

'postgresql://{username}:{password}@localhost:{port}/{database_name}'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://master:ekka@localhost:5432/StudentTemplateDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = SQLAlchemy(app)

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image1 = db.Column(db.String(100), nullable=False)
    image2 = db.Column(db.String(100), nullable=False)
    image3 = db.Column(db.String(100), nullable=False)
    image4 = db.Column(db.String(100), nullable=False)
    image5 = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000))
    price = db.Column(db.Numeric(10, 2), nullable=False)
    specification = db.Column(db.String(10))
    
class Team(db.Model):
    __tablename__ = 'team'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.String(1000), nullable=False)
    image = db.Column(db.String(100), nullable=False)
    occupation = db.Column(db.String(250), nullable=False)
    facebook_link = db.Column(db.String(1000))
    
    twitter_link = db.Column(db.String(1000))



@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/product')
def product():
    products = Product.query.all()
    return render_template('product.html', products=products)

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/product/<int:id>/details', methods=['GET'])
def product_details(id):
    products = Product.query.get(id)
    return render_template('single.html', products=products)

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        # Extract other form fields as needed
        image1 = request.files.get('image1')
        image2 = request.files.get('image2')
        image3 = request.files.get('image3')
        image4 = request.files.get('image4')
        image5 = request.files.get('image5')
        # Read image file as bytes

        description = request.form['description']
        price = request.form['price']
        specification = request.form['specification']

        # Create a new Product instance
        new_product = Product(name=name, description=description, price=price, specification=specification)

        # Handle the updated image file
        if image1:
            filename = secure_filename(image1.filename)
            image1.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new_product.image1 = filename
            
        if image2:
            filename = secure_filename(image2.filename)
            image2.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new_product.image2 = filename
        
        if image3:
            filename = secure_filename(image3.filename)
            image3.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new_product.image3 = filename
            
        if image4:
            filename = secure_filename(image4.filename)
            image4.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new_product.image4 = filename
            
        if image5:
            filename = secure_filename(image5.filename)
            image5.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new_product.image5 = filename

        # Add and commit the new product to the database
        db.session.add(new_product)
        db.session.commit()
        
        return redirect(url_for('add_product'))  # Redirect to the add_product page after submission
    
    return render_template('add_product.html')

@app.route('/add_team', methods=['GET', 'POST'])      
def add_team():
    if request.method == 'POST':
        name = request.form['name']
        # Extract other form fields as needed
        bio = request.form['bio']
        image = request.files.get('image')
        occupation = request.form['occupation']
        facebook_link = request.form['facebook_link']
        twitter_link = request.form['twitter_link']
        
        # Create a new Team instance
        new_team = Team(name=name, bio=bio, occupation=occupation, facebook_link=facebook_link, twitter_link=twitter_link)
        
        # Handle the updated image file
        if image:
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new_team.image = filename
        
        # Add and commit the new team to the database
        db.session.add(new_team)
        db.session.commit()
        
        return redirect(url_for('add_team'))  # Redirect to the add_team page after submission
    
    return render_template('add_team.html')


# Edit Data in Database routes
@app.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    product = Product.query.get(product_id)

    if request.method == 'POST':
        product.name = request.form['name']
        # Handle updated images
        updated_images = request.files.getlist('image')
        image_bytes_list = []

        for image in updated_images:
            image_bytes_list.append(image.read())

        product.images = image_bytes_list  # Update the images attribute
        product.occupation = request.form['occupation']
        product.specification = request.form['specification']
        product.description = request.form['description']
        # Update other fields as needed
        
        db.session.commit()
        return redirect(url_for('edit_product', product_id=product.id))  # Redirect to the same edit page after update
    
    return render_template('edit-product.html', product=product)

@app.route('/edit_team/<int:team_id>', methods=['GET', 'POST'])
def edit_team(team_id):
    team = Team.query.get(team_id)

    if request.method == 'POST':
        team.name = request.form['name']
        team.bio = request.form['bio']
        team.image = request.form['image']
        team.twitter_link = request.form['twitter_link']
        team.facebook_link = request.form['facebook_link']
        # Update other fields as needed
        
        db.session.commit()
        return redirect(url_for('edit_team', team_id=team.id))  # Redirect to the same edit page after update
    
    return render_template('edit-team.html', team=team)

# View Data in Database
@app.route('/admin-index')
def admin_index():
    return render_template('admin-index.html')

@app.route('/admin_team')
def admin_team():
    teams = Team.query.all()  # Fetch all teams from the database
    return render_template('admin-team.html', teams=teams)

@app.route('/admin_product')
def admin_product():
    products = Product.query.all()  # Fetch all products from the database
    return render_template('admin-product.html', products=products)

# Delete property
@app.route('/products/<int:id>/delete', methods=['GET', 'DELETE'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash("Product deleted successfully")
    return redirect(url_for('index'))




if __name__ == "__main__":
    app.run(debug = True)
  