import requests

# URL base da API
url_base = "http://127.0.0.1:5000"

print("--- INICIANDO TESTES DA ATIVIDADE ---")

# 1. Cadastrar um usuario para teste
dados_cadastro = {
    "nome": "Joao Silva",
    "email": "joao@email.com",
    "senha": "123"
}
res = requests.post(f"{url_base}/users/", json=dados_cadastro)
print("Cadastro:", res.status_code, res.json())

# 2. Fazer login para pegar o token
dados_login = {
    "email": "joao@email.com",
    "senha": "123"
}
res_login = requests.post(f"{url_base}/users/login", json=dados_login)
token = res_login.json().get("access_token")
print("Token gerado:", token)

# Header com o token para as rotas protegidas
headers = {
    "Authorization": f"Bearer {token}"
}

# 3. Criar um formulario para podermos testar o GET, PUT e DELETE depois
dados_form = {
    "titulo": "Formulario de Pesquisa",
    "descricao": "Pesquisa de satisfacao do cliente"
}
res_form = requests.post(f"{url_base}/formularios/", json=dados_form, headers=headers)
print("Criar Formulario:", res_form.status_code, res_form.json())

print("\n================ TESTES DE FORMULARIOS ================")

# GET Formulario
print("\n--- GET /formularios/1 ---")
# Com token
r1 = requests.get(f"{url_base}/formularios/1", headers=headers)
print("[COM TOKEN] Status:", r1.status_code, "| Resposta:", r1.json())

# Sem token
r2 = requests.get(f"{url_base}/formularios/1")
print("[SEM TOKEN] Status:", r2.status_code, "| Resposta:", r2.json())

# Registro nao existe
r3 = requests.get(f"{url_base}/formularios/999", headers=headers)
print("[INEXISTENTE] Status:", r3.status_code, "| Resposta:", r3.json())


# PUT Formulario
print("\n--- PUT /formularios/1 ---")
# Com token
dados_update_form = {"titulo": "Formulario Editado"}
r1 = requests.put(f"{url_base}/formularios/1", json=dados_update_form, headers=headers)
print("[COM TOKEN] Status:", r1.status_code, "| Resposta:", r1.json())

# Sem token
r2 = requests.put(f"{url_base}/formularios/1", json=dados_update_form)
print("[SEM TOKEN] Status:", r2.status_code, "| Resposta:", r2.json())

# Registro nao existe
r3 = requests.put(f"{url_base}/formularios/999", json=dados_update_form, headers=headers)
print("[INEXISTENTE] Status:", r3.status_code, "| Resposta:", r3.json())


# DELETE Formulario
print("\n--- DELETE /formularios/1 ---")
# Sem token (testando o bloqueio antes de deletar de verdade)
r2 = requests.delete(f"{url_base}/formularios/1")
print("[SEM TOKEN] Status:", r2.status_code, "| Resposta:", r2.json())

# Registro nao existe
r3 = requests.delete(f"{url_base}/formularios/999", headers=headers)
print("[INEXISTENTE] Status:", r3.status_code, "| Resposta:", r3.json())

# Com token (deleta de fato)
r1 = requests.delete(f"{url_base}/formularios/1", headers=headers)
print("[COM TOKEN] Status:", r1.status_code, "| Resposta:", r1.json())


print("\n================ TESTES DE USUARIOS ================")

# GET Usuario
print("\n--- GET /users/1 ---")
# Com token
r1 = requests.get(f"{url_base}/users/1", headers=headers)
print("[COM TOKEN] Status:", r1.status_code, "| Resposta:", r1.json())

# Sem token
r2 = requests.get(f"{url_base}/users/1")
print("[SEM TOKEN] Status:", r2.status_code, "| Resposta:", r2.json())

# Registro nao existe
r3 = requests.get(f"{url_base}/users/999", headers=headers)
print("[INEXISTENTE] Status:", r3.status_code, "| Resposta:", r3.json())


# PUT Usuario
print("\n--- PUT /users/1 ---")
# Com token
dados_update_user = {"nome": "Joao Silva Editado"}
r1 = requests.put(f"{url_base}/users/1", json=dados_update_user, headers=headers)
print("[COM TOKEN] Status:", r1.status_code, "| Resposta:", r1.json())

# Sem token
r2 = requests.put(f"{url_base}/users/1", json=dados_update_user)
print("[SEM TOKEN] Status:", r2.status_code, "| Resposta:", r2.json())

# Registro nao existe
r3 = requests.put(f"{url_base}/users/999", json=dados_update_user, headers=headers)
print("[INEXISTENTE] Status:", r3.status_code, "| Resposta:", r3.json())


# DELETE Usuario
print("\n--- DELETE /users/1 ---")
# Sem token
r2 = requests.delete(f"{url_base}/users/1")
print("[SEM TOKEN] Status:", r2.status_code, "| Resposta:", r2.json())

# Registro nao existe
r3 = requests.delete(f"{url_base}/users/999", headers=headers)
print("[INEXISTENTE] Status:", r3.status_code, "| Resposta:", r3.json())

# Com token
r1 = requests.delete(f"{url_base}/users/1", headers=headers)
print("[COM TOKEN] Status:", r1.status_code, "| Resposta:", r1.json())

print("\n--- FIM DOS TESTES ---")