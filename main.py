
# Importar
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Conectando SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Creando una base de datos
db = SQLAlchemy(app)

# Creación de una tabla
class Card(db.Model):
    # Creación de columnas
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    subtitle = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)

    # Salida del objeto y del id
    def __repr__(self):
        return f'<Card {self.id}>'

# Creación de la tabla Usuario
class User(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   login = db.Column(db.String(100), nullable=False)
   password = db.Column(db.String(100), nullable=False)  # Aumenta el tamaño máximo del password

# Asegurarse de que las tablas están creadas
with app.app_context():
    db.create_all()

# Ejecutar la página de contenidos
@app.route('/', methods=['GET', 'POST'])
def login():
    error = ''
    if request.method == 'POST':
        form_login = request.form['email']
        form_password = request.form['password']
        
        # Aplicar la autorización
        user_db = User.query.all()
        for user in user_db:
            if form_login == user.login and form_password == user.password:
                return redirect("/index")
        else:
            error = "Tu usuario y/o contraseña no coincide"
            return render_template('login.html', error=error)
        
    else:
        return render_template('login.html')

@app.route('/reg', methods=['GET', 'POST'])
def reg():
    if request.method == 'POST':
        login = request.form['email']
        password = request.form['password']
        
        # Registro de usuario
        user = User(login=login, password=password)
        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()  # Revertir cambios si hay un error
            return f"Error al registrar el usuario: {e}"
        
        return redirect('/')
    else:    
        return render_template('registration.html')

# Ejecutar la página de contenidos
@app.route('/index')
def index():
    # Visualización de las entradas de la base de datos
    cards = Card.query.order_by(Card.id).all()
    return render_template('index.html', cards=cards)

# Ejecutar la página con la entrada
@app.route('/card/<int:id>')
def card(id):
    card = Card.query.get(id)
    return render_template('card.html', card=card)

# Ejecutar la página de creación de entradas
@app.route('/create')
def create():
    return render_template('create_card.html')

# El formulario de inscripción
@app.route('/form_create', methods=['GET', 'POST'])
def form_create():
    if request.method == 'POST':
        title = request.form['title']
        subtitle = request.form['subtitle']
        text = request.form['text']

        # Creación de un objeto que se enviará a la base de datos
        card = Card(title=title, subtitle=subtitle, text=text)

        try:
            db.session.add(card)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return f"Error al crear la entrada: {e}"
        
        return redirect('/index')
    else:
        return render_template('create_card.html')

if __name__ == "__main__":
    app.run(debug=True)
