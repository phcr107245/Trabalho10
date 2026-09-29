from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required

app = Flask(__name__)

# Configuracao do banco sqlite e do jwt
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meubanco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'minha_chave_secreta_123'

db = SQLAlchemy(app)
jwt = JWTManager(app)

# Modelos do banco de dados
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    senha = db.Column(db.String(100))

class Formulario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100))
    descricao = db.Column(db.String(200))

# Criar as tabelas
with app.app_context():
    db.create_all()

# ==========================================
# ROTAS DE USUARIOS
# ==========================================

# Cadastrar usuario
@app.route('/users/', methods=['POST'])
def cadastrar_usuario():
    dados = request.get_json()
    
    # Verifica se o email ja existe
    usuario_existente = User.query.filter_by(email=dados['email']).first()
    if usuario_existente:
        return jsonify({"mensagem": "Email ja cadastrado"}), 400
        
    novo_user = User(
        nome=dados['nome'],
        email=dados['email'],
        senha=dados['senha']
    )
    
    db.session.add(novo_user)
    db.session.commit()
    
    return jsonify({"mensagem": "Usuario cadastrado com sucesso!"}), 201

# Login do usuario
@app.route('/users/login', methods=['POST'])
def login():
    dados = request.get_json()
    usuario = User.query.filter_by(email=dados['email'], senha=dados['senha']).first()
    
    if usuario:
        # Gera o token passando o ID do usuario
        token = create_access_token(identity=str(usuario.id))
        return jsonify({"access_token": token}), 200
    else:
        return jsonify({"mensagem": "Email ou senha incorretos"}), 401

# Consultar usuario por ID (Protegido)
@app.route('/users/<int:id>', methods=['GET'])
@jwt_required()
def buscar_usuario(id):
    usuario = User.query.get(id)
    
    if not usuario:
        return jsonify({"mensagem": "Usuario nao encontrado"}), 404
        
    return jsonify({
        "id": usuario.id,
        "nome": usuario.nome,
        "email": usuario.email
    }), 200

# Atualizar usuario (Protegido)
@app.route('/users/<int:id>', methods=['PUT'])
@jwt_required()
def atualizar_usuario(id):
    usuario = User.query.get(id)
    
    if not usuario:
        return jsonify({"mensagem": "Usuario nao encontrado"}), 404
        
    dados = request.get_json()
    
    if 'nome' in dados:
        usuario.nome = dados['nome']
    if 'email' in dados:
        usuario.email = dados['email']
    if 'senha' in dados:
        usuario.senha = dados['senha']
        
    db.session.commit()
    return jsonify({"mensagem": "Usuario atualizado com sucesso!"}), 200

# Deletar usuario (Protegido)
@app.route('/users/<int:id>', methods=['DELETE'])
@jwt_required()
def deletar_usuario(id):
    usuario = User.query.get(id)
    
    if not usuario:
        return jsonify({"mensagem": "Usuario nao encontrado"}), 404
        
    db.session.delete(usuario)
    db.session.commit()
    return jsonify({"mensagem": "Usuario excluido com sucesso!"}), 200


# ==========================================
# ROTAS DE FORMULARIOS
# ==========================================

# Criar formulario (Protegido)
@app.route('/formularios/', methods=['POST'])
@jwt_required()
def criar_formulario():
    dados = request.get_json()
    
    novo_form = Formulario(
        titulo=dados['titulo'],
        descricao=dados['descricao']
    )
    
    db.session.add(novo_form)
    db.session.commit()
    
    return jsonify({
        "mensagem": "Formulario criado com sucesso!",
        "id": novo_form.id
    }), 201

# Consultar formulario por ID (Protegido)
@app.route('/formularios/<int:id>', methods=['GET'])
@jwt_required()
def buscar_formulario(id):
    form = Formulario.query.get(id)
    
    if not form:
        return jsonify({"mensagem": "Formulario nao encontrado"}), 404
        
    return jsonify({
        "id": form.id,
        "titulo": form.titulo,
        "descricao": form.descricao
    }), 200

# Atualizar formulario (Protegido)
@app.route('/formularios/<int:id>', methods=['PUT'])
@jwt_required()
def atualizar_formulario(id):
    form = Formulario.query.get(id)
    
    if not form:
        return jsonify({"mensagem": "Formulario nao encontrado"}), 404
        
    dados = request.get_json()
    
    if 'titulo' in dados:
        form.titulo = dados['titulo']
    if 'descricao' in dados:
        form.descricao = dados['descricao']
        
    db.session.commit()
    return jsonify({"mensagem": "Formulario atualizado com sucesso!"}), 200

# Deletar formulario (Protegido)
@app.route('/formularios/<int:id>', methods=['DELETE'])
@jwt_required()
def deletar_formulario(id):
    form = Formulario.query.get(id)
    
    if not form:
        return jsonify({"mensagem": "Formulario nao encontrado"}), 404
        
    db.session.delete(form)
    db.session.commit()
    return jsonify({"mensagem": "Formulario excluido com sucesso!"}), 200

if __name__ == '__main__':
    app.run(debug=True)